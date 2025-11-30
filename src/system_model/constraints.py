import numpy as np

def enforce_power_constraint(W, p_max_dbm):
    """
    Chuẩn hóa ma trận Beamforming để thỏa mãn ràng buộc công suất tại mỗi AP.
    
    Args:
        W: Ma trận Beamforming hiện tại (M, K, N) - Số phức
        p_max_dbm: Công suất tối đa (dBm)
        
    Returns:
        W_normalized: Ma trận đã được chuẩn hóa
    """
    # Chuyển đổi dBm sang Watts
    p_max_watts = 10**((p_max_dbm - 30) / 10)
    
    M, K, N = W.shape
    W_norm = W.copy()
    
    # Duyệt qua từng AP để kiểm tra
    for m in range(M):
        # Tính tổng công suất phát của AP m dành cho tất cả K users
        # P_total = sum(|w_m1|^2 + |w_m2|^2 + ... + |w_mK|^2)
        # np.linalg.norm(vector)**2 tính tổng bình phương module
        
        # Flatten w[m, :, :] thành 1 vector dài K*N để tính tổng năng lượng nhanh
        power_current = np.sum(np.abs(W[m, :, :])**2)
        
        # Nếu công suất vượt quá giới hạn -> Scale down
        if power_current > p_max_watts:
            scale_factor = np.sqrt(p_max_watts / power_current)
            W_norm[m, :, :] *= scale_factor
            
    return W_norm