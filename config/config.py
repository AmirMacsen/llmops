class Config:
    def __init__(self):
        # 关闭wtf的csrf校验
        self.WTF_CSRF_ENABLED = False
