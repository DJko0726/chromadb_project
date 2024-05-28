import csv
import os
 
class Csv:
    def __init__(self,timestamp):
        self.file_path=f'./download_file/csv/{timestamp}.csv'
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
    def download(self, data):
        try:
            with open(self.file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data.keys())
                writer.writerows(zip(*data.values()))
            return self.file_path
        except Exception as e:
            print(f"Error while searching: {e}")
            return None
            
    
