import gspread
import os
import sys

class MysheetLib:

    #---------------------------------------------------------------------
    def get_google_sheet_data(self, json_keyfile, file_name, sheet_name):
        try:
            # get into google sheet
            gc = gspread.service_account(filename=json_keyfile)

            # open file name
            sh = gc.open(file_name)

            # Open work sheet
            worksheet = sh.worksheet(sheet_name)

            # get data
            # ⚠️ แก้ไข: ต้องมีวงเล็บ () ต่อท้าย ไม่งั้นจะได้ object แทนข้อมูล
            data = worksheet.get_all_records() 

            return data
        
        except Exception as e:
            print(f"error log : {e}")
            return []

    #---------------------------------------------------------------------
    def _get_worksheet(self, json_keyfile, file_name, sheet_name):
        gc = gspread.service_account(filename=json_keyfile)
        sh = gc.open(file_name)
        return sh.worksheet(sheet_name)
    
    # แบบที่ 1: ดึงมาเป็น Dictionary
    def get_all_records(self, json_keyfile, file_name, sheet_name):
        ws = self._get_worksheet(json_keyfile, file_name, sheet_name)
        return ws.get_all_records()

    # แบบที่ 2: ดึงมาเป็น List ซ้อน List
    def get_all_values(self, json_keyfile, file_name, sheet_name):
        ws = self._get_worksheet(json_keyfile, file_name, sheet_name)
        return ws.get_all_values()

    # แบบที่ 3: ดึงค่าจากเซลล์เดียว
    def get_cell_value(self, json_keyfile, file_name, sheet_name, cell_address):
        ws = self._get_worksheet(json_keyfile, file_name, sheet_name)
        return ws.acell(cell_address).value
    
    #---------------------------------------------------------------------
    def get_all_sheet_names(self, json_keyfile, file_name):
        gc = gspread.service_account(filename=json_keyfile)
        sh = gc.open(file_name)
        
        # วนลูปดึงชื่อ (Title) ของทุก Worksheet ออกมา
        sheet_names = [ws.title for ws in sh.worksheets()]
        return sheet_names

    # (แถม) ดึงชื่อไฟล์ Spreadsheet
    def get_spreadsheet_name(self, json_keyfile, file_name):
        gc = gspread.service_account(filename=json_keyfile)
        sh = gc.open_by_key(file_name)
        return sh.title

# ==========================================
# ส่วนสั่งรัน (Main Block) - จะทำงานเมื่อกด Run ไฟล์นี้
# ==========================================
if __name__ == "__main__":
    
    # 1. ตั้งค่า Path ให้แม่นยำ (ป้องกันหาไฟล์ไม่เจอ)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # ⚠️ แก้ชื่อไฟล์ JSON ตรงนี้ให้ตรงกับของคุณ
    # ถ้าไฟล์อยู่ในโฟลเดอร์ secure ให้ใส่ 'secure/ชื่อไฟล์.json'
    json_filename = "service_account.json" 
    Json_path = os.path.join(current_dir, json_filename)
    
    # ⚠️ แก้ชื่อ Google Sheet ตรงนี้
    Sheet_name = "RobotTestData" 

    print(f"--- กำลังทดสอบเชื่อมต่อ ---")
    print(f"File: {Sheet_name}")
    print(f"Key : {Json_path}")

    # 2. สร้าง Object
    mybot = MysheetLib()

    try:
        # 3. ลองดึงรายชื่อ Tab
        print("\nSending request...")
        tab_names = mybot.get_all_sheet_names(Json_path, Sheet_name)
        
        print("\n✅ สำเร็จ! รายชื่อ Tab ทั้งหมด:")
        print(tab_names)
        
        # 4. (แถม) ลองดึงข้อมูลจาก Tab แรก
        if tab_names:
            first_tab = tab_names[0]
            print(f"\nExample data from '{first_tab}':")
            data = mybot.get_all_records(Json_path, Sheet_name, first_tab)
            print(data)

    except Exception as e:
        print(f"\n❌ Error log : {e}")