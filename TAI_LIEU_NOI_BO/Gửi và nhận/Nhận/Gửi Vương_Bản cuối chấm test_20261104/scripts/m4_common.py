"""Hàm dùng chung Chương 4 (phần Vương): giỏ, phép che, danh mục C, khai phá luật.

Mọi thống kê học từ reference; giỏ fit/validation/test chỉ được che, không dùng để học luật.

ĐỌC NHANH (vấn đáp). File này là NỀN của Chương 4, sáu nhóm theo thứ tự dùng:
  1. Giỏ và phép che: baskets, mask (che h = min(k-1, max(1, floor(0,2k))) sản phẩm, seed + order_id).
  2. Danh mục C và luật: catalog (xếp sản phẩm theo độ phổ biến), basket_matrix, mine (Apriori/FP-Growth), rules.
  3. So sánh Apriori và FP-Growth: cùng tập itemset, support lệch <= 1e-12.
  4. Đặc trưng ứng viên: index_rules + basket_features (tra luật bằng tìm kiếm nhị phân, ứng viên không khớp luật = 0).
  5. Chấm điểm: make_batches (lô giỏ), sample_negatives (20 mẫu âm/giỏ), evaluate (P@k, R@k, HR@10, trần Recall@10).
  6. locked_stage: nạp lại cấu hình giai đoạn A đã chọn, CHỈ fit/validation, test không được nạp.
  Ba ý quan trọng: hàm đặc trưng chỉ dùng phần quan sát O, không dùng phần bị che H; ứng viên = C trừ O;
  mọi phương pháp xếp hạng cùng một quy tắc hòa (product_id tăng).
"""
import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth
from scipy import sparse

from project_io import check_hashes, path, read_json, require

# Đường dẫn cấu hình và tệp hash của Chương 4.
CONFIG = "configs/m4_model.json"
HASHES = "DATA/Data phai sinh/M4/hashes.json"


def config():
    return read_json(path(CONFIG))


def mask_params(cfg):
    return {"seed": cfg["seeds"]["mask"], "hidden_share": cfg["hidden_share"]}


def check_mask(record, cfg):
    """Dừng nếu phép che đã lưu không được tạo từ tham số che trong config hiện tại."""
    require(record.get("mask") == mask_params(cfg), "Phép che đã lưu khác config; chạy lại m4_prepare.py")


# ===== Nhóm 1: dựng giỏ và phép che =====
def baskets(master, split, splits):
    """Một dòng mỗi giỏ của các tập `splits`; `items` là danh sách product_id tăng dần."""
    users = split.loc[split.split.isin(splits)].set_index("user_id").split
    rows = master.loc[master.user_id.isin(users.index), ["order_id", "user_id", "product_id"]]
    out = (rows.sort_values(["order_id", "product_id"])
           .groupby("order_id", sort=True).agg(user_id=("user_id", "first"),
                                               items=("product_id", list)).reset_index())
    out["split"] = out.user_id.map(users).astype(str)
    require(not out.user_id.duplicated().any(), "Mỗi người dùng phải có đúng một giỏ")
    return out


def mask(items, order_id, seed=42, share=0.2):
    """Che h = min(k-1, max(1, floor(share*k))) sản phẩm; giỏ k < 2 không che (Chương 2)."""
    k = len(items)
    if k < 2:
        return list(items), []
    h = min(k - 1, max(1, int(np.floor(share * k))))
    hidden = np.random.default_rng([seed, order_id]).choice(np.asarray(items), h, replace=False)
    hidden = sorted(int(x) for x in hidden)
    return [int(x) for x in items if x not in hidden], hidden


# ===== Nhóm 2: danh mục C và khai phá luật (chỉ học trên reference) =====
def catalog(reference):
    """Mọi sản phẩm của reference, xếp theo số giỏ chứa giảm dần, phá hòa product_id tăng.

    Danh mục C với Top-N là các dòng rank <= N. Mẫu số popularity là toàn bộ giỏ reference.
    """
    n_baskets = reference.order_id.nunique()
    out = (reference.groupby("product_id").agg(n_ref=("order_id", "nunique"),
                                               department_id=("department_id", "first"))
           .reset_index().sort_values(["n_ref", "product_id"], ascending=[False, True]))
    out["popularity"] = out.n_ref / n_baskets
    out["rank"] = np.arange(1, len(out) + 1)
    return out.reset_index(drop=True)


def basket_matrix(reference, products):
    """Ma trận Boolean thưa: hàng = mọi giỏ reference (kể cả giỏ không có sản phẩm nào của C)."""
    rows, order_ids = pd.factorize(reference.order_id, sort=True)
    column = pd.Index(products)
    keep = column.get_indexer(reference.product_id) >= 0
    data = sparse.csr_matrix((np.ones(keep.sum(), dtype=bool),
                              (rows[keep], column.get_indexer(reference.product_id[keep]))),
                             shape=(len(order_ids), len(column)))
    # mlxtend yêu cầu tên cột chuỗi với DataFrame thưa; kết quả đổi lại về int.
    return pd.DataFrame.sparse.from_spmatrix(data, columns=[str(int(p)) for p in products])


def mine(matrix, algorithm, min_count, max_len):
    """Itemset phổ biến với support >= min_count/N; cùng đầu vào cho Apriori và FP-Growth."""
    support = min_count / len(matrix)
    if algorithm == "apriori":  # mặc định cần ~14 GB RAM ở N=500 (lượt thử 01/11); low_memory cho cùng kết quả
        return apriori(matrix, min_support=support, use_colnames=True, max_len=max_len, low_memory=True)
    return fpgrowth(matrix, min_support=support, use_colnames=True, max_len=max_len)


def rules(itemsets, n_baskets, min_confidence):
    """Luật hậu đề một sản phẩm, kèm số giỏ đếm được để báo cùng tỷ lệ."""
    found = association_rules(itemsets, num_itemsets=n_baskets, metric="confidence",
                              min_threshold=min_confidence)
    found = found.loc[found.consequents.map(len) == 1]
    out = pd.DataFrame({
        "antecedent": found.antecedents.map(lambda s: sorted(int(x) for x in s)),
        "consequent": found.consequents.map(lambda s: int(next(iter(s)))),
        "n_antecedent": (found["antecedent support"] * n_baskets).round().astype(int),
        "n_both": (found.support * n_baskets).round().astype(int),
        **{c: found[c] for c in ["support", "confidence", "lift", "leverage", "conviction"]}})
    return out.sort_values(["consequent", "confidence"], ascending=[True, False]).reset_index(drop=True)


# ===== Nhóm 3: so sánh Apriori và FP-Growth =====
def itemset_signature(itemsets):
    """{itemset đã sắp: support chưa làm tròn} để so Apriori và FP-Growth."""
    return {tuple(sorted(int(x) for x in s)): float(v)
            for s, v in zip(itemsets.itemsets, itemsets.support)}


def max_support_gap(a, b):
    """Sai số support lớn nhất giữa hai kết quả; None nếu tập itemset khác nhau."""
    return max((abs(a[k] - b[k]) for k in a), default=0.0) if a.keys() == b.keys() else None


def worst_support_gap(runs):
    """Sai số lớn nhất của mọi lượt so với lượt đầu; None nếu rỗng hoặc có lượt khác tập itemset."""
    gaps = [max_support_gap(runs[0], r) for r in runs] if runs else [None]
    return None if None in gaps else max(gaps)


# ===== Nhóm 4: đặc trưng ứng viên (khớp luật bằng tìm kiếm nhị phân) =====
M = 1 << 16  # product_id < 65.536: khóa luật = đầu tiên * M + thứ hai (0 nếu chỉ một sản phẩm)


def context(ranked, n, dept):
    """C = Top-n của danh mục theo thứ tự xếp hạng; pos[product_id] là vị trí trong C (-1 nếu ngoài C)."""
    top = ranked[ranked["rank"] <= n]
    pos = np.full(M, -1)
    pos[top.product_id] = np.arange(len(top))
    return {"pid": top.product_id.to_numpy(), "pop": top.popularity.to_numpy(),
            "dept": top.department_id.to_numpy(), "pos": pos, "all_dept": dept}


def index_rules(found, ctx):
    """Chỉ mục luật theo tiền đề: các luật cùng tiền đề nằm liền nhau trong cons/conf/lift."""
    key = found.antecedent.map(lambda s: s[0] * M + (s[1] if len(s) > 1 else 0)).to_numpy()
    order = np.argsort(key, kind="stable")
    unique, start = np.unique(key[order], return_index=True)
    return {"uk": unique, "start": start, "end": np.append(start[1:], len(key)),
            "pairs": bool((found.antecedent.map(len) > 1).any()),
            "cons": ctx["pos"][found.consequent.to_numpy()][order],
            "conf": found.confidence.to_numpy()[order], "lift": found.lift.to_numpy()[order]}


def basket_features(observed, ctx, idx):
    """Bảy đặc trưng của mọi ứng viên trong C trừ O theo thứ tự danh mục; chỉ dùng O, không dùng H."""
    obs = np.asarray(observed, dtype=np.int64)
    # Bước 1: sản phẩm quan sát nằm trong C; khóa tiền đề một sản phẩm = a*M, cặp = a*M + b.
    inside = obs[ctx["pos"][obs] >= 0]
    keys = inside * M
    if idx["pairs"] and len(inside) > 1:
        i, j = np.triu_indices(len(inside), 1)
        keys = np.append(keys, inside[i] * M + inside[j])
    # Bước 2: tra khóa tiền đề trong chỉ mục luật bằng tìm kiếm nhị phân.
    loc = np.searchsorted(idx["uk"], keys).clip(max=len(idx["uk"]) - 1)
    loc = loc[idx["uk"][loc] == keys]
    rows = np.concatenate([np.arange(idx["start"][k], idx["end"][k]) for k in loc] or [np.empty(0, int)])
    # Bước 3: mỗi ứng viên: đếm số luật khớp, lấy confidence và lift LỚN NHẤT; không khớp luật nào thì bằng 0 (không để thiếu).
    n, cons = len(ctx["pid"]), idx["cons"][rows]
    count, conf, lift = np.bincount(cons, minlength=n).astype(float), np.zeros(n), np.zeros(n)
    np.maximum.at(conf, cons, idx["conf"][rows])
    np.maximum.at(lift, cons, idx["lift"][rows])
    # Bước 4: loại sản phẩm đã có trong giỏ khỏi ứng viên (C trừ O).
    keep = np.ones(n, bool)
    keep[ctx["pos"][inside]] = False
    same = np.bincount(ctx["all_dept"][obs], minlength=22)[ctx["dept"]]
    features = {"product_id": ctx["pid"], "candidate_popularity": ctx["pop"], "matching_rule_count": count,
                "max_rule_confidence": conf, "max_rule_lift": lift,
                "observed_basket_size": np.full(n, float(len(obs))), "same_department_count": same.astype(float),
                "candidate_department_id": ctx["dept"].astype(float)}
    return {name: value[keep] for name, value in features.items()}


# ===== Nhóm 5: chấm điểm xếp hạng =====
def make_batches(frame, ctx, idx, size):
    """Sinh (giỏ, bảng ứng viên) theo lô; X có đặc trưng, `basket` (chỉ số trong lô) và nhãn `y` (thuộc H)."""
    for start in range(0, len(frame), size):
        part = frame.iloc[start:start + size].reset_index(drop=True)
        feats = [basket_features(o, ctx, idx) for o in part.observed]
        X = pd.DataFrame({c: np.concatenate([f[c] for f in feats]) for c in feats[0]})
        X["basket"] = np.repeat(np.arange(len(part)), [len(f["product_id"]) for f in feats])
        hidden = np.concatenate([b * M + np.asarray(h, dtype=np.int64) for b, h in enumerate(part.hidden)])
        X["y"] = np.isin(X.basket.to_numpy() * M + X.product_id.to_numpy(), hidden)
        yield part, X


def sample_negatives(part, X, n, seed):
    """Giữ mọi dòng dương và tối đa n dòng âm mỗi giỏ (RNG riêng theo order_id, không hoàn lại)."""
    y, edges = X.y.to_numpy(), np.searchsorted(X.basket.to_numpy(), np.arange(len(part) + 1))
    keep = [np.flatnonzero(y)]
    for b, order_id in enumerate(part.order_id):
        negative = np.flatnonzero(~y[edges[b]:edges[b + 1]]) + edges[b]
        keep.append(np.random.default_rng([seed, order_id]).choice(negative, min(n, len(negative)), replace=False))
    out = X.iloc[np.sort(np.concatenate(keep))]
    return out.assign(order_id=part.order_id.to_numpy()[out.basket.to_numpy()])


def evaluate(part, X, *keys, ks=(5, 10)):
    """Chỉ số theo giỏ của một phương pháp; `keys` là các khóa giảm dần theo thứ tự ưu tiên, hòa thì product_id tăng."""
    # Xếp hạng trong từng giỏ theo các khóa giảm dần; hòa thì product_id tăng.
    order = np.lexsort((X.product_id.to_numpy(), *[-np.asarray(k, float) for k in keys[::-1]], X.basket.to_numpy()))
    basket, hit = X.basket.to_numpy()[order], X.y.to_numpy()[order]
    place = np.arange(len(order)) - np.searchsorted(basket, basket)
    n, h = len(part), part.hidden.map(len).to_numpy()
    out = part[["order_id", "user_id"]].copy()
    out["n_hidden"], out["n_hidden_in_C"] = h, np.bincount(X.basket.to_numpy()[X.y.to_numpy()], minlength=n)
    # P@k = trúng/k; R@k = trúng/|H| (|H| gồm cả sản phẩm ngoài C); trần Recall@10 = min(|H giao C|, 10)/|H|.
    for k in ks:
        hits = np.bincount(basket[hit & (place < k)], minlength=n)
        out[f"hits@{k}"], out[f"P@{k}"], out[f"R@{k}"] = hits, hits / k, hits / h
    out[f"HR@{ks[-1]}"] = (out[f"hits@{ks[-1]}"] > 0).astype(float)
    out[f"R@{ks[-1]}_ceiling"] = np.minimum(out.n_hidden_in_C, ks[-1]) / h
    return out


# ===== Nhóm 6: nạp lại cấu hình giai đoạn A đã chọn (test KHÔNG được nạp) =====
def locked_stage(cfg, splits=("fit", "validation")):
    """Giỏ của các tập `splits` (mặc định fit/validation, test không được nạp), ngữ cảnh và chỉ mục luật của cấu hình A đã chọn.

    Chỉ bước chấm test sau khóa (m4_test.py) được truyền splits=("test",)."""
    record = check_hashes(HASHES)
    check_mask(record, cfg)
    data, a = path(cfg["data_dir"]), record["stage_A"]
    masked = pd.read_parquet(data / "masked_baskets.parquet", filters=[("split", "in", list(splits))])
    found = pd.read_parquet(data / "rules_grid.parquet")
    found = found[(found.top_n == a["top_n"]) & (found.min_count == a["min_count"]) & (found.max_len == a["max_len"])
                  & (found.confidence >= a["min_confidence"])]
    master = pd.read_parquet(path("DATA/Data đã làm sạch/master_train.parquet"), columns=["product_id", "department_id"])
    dept = np.zeros(M, dtype=int)
    dept[master.product_id.to_numpy()] = master.department_id.to_numpy()
    ctx = context(pd.read_parquet(data / "catalog.parquet"), a["top_n"], dept)
    return masked, ctx, index_rules(found, ctx), record
