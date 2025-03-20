import torch
import ctypes


"""NVIDIA CUDA GPU"""
# if torch.cuda.is_available():
#     torch.cuda.empty_cache()  # 清空CUDA缓存
#     torch.cuda.ipc_collect()  # 释放IPC内存

"""Apple Silicon"""
if torch.backends.mps.is_available():
    torch.mps.empty_cache()  # 清空MPS缓存
    torch.mps.dismiss_cache()  # 释放MPS保留内存

"""纯CPU"""
# # 通常无需额外操作，但可强制释放内存
# libc = ctypes.CDLL("libc.dylib")  # macOS/Linux
# libc.malloc_trim(0)              # 主动归还内存给系统