import pandas as pd
import os

class Excel:
    def __init__(self,timestamp):
        self.file_path=f'./download_file/excel/{timestamp}.xlsx'
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
    def download(self, data):
        try:
            df = pd.DataFrame(data)
            df.to_excel(self.file_path, index=False)
            return self.file_path
        except Exception as e:
            print(f"Error while searching: {e}")
            return None