import os
import sys
from MySheetLib import MysheetLib  
from MyFileLib  import MyFileLib

current_dir = os.path.dirname(os.path.abspath(__file__))
Json_path = os.path.join(current_dir, 'secure', 'service_account.json')

Sheet_name = 'Oxford_3000_Sorted' 
output_filename = 'txt_save_output'

def get_worksheet_and_save_file(Json_path,Sheet_name,file_name,output_filename):
    # สร้างหุ่นยนต์
    mybot = MysheetLib()

    #สร้างตัวเก็บไฟล์
    mf = MyFileLib()

    try:
        print(f"Connecting to: {Sheet_name}...")
        print(f"Using Key: {Json_path}")

        # เรียกใช้ฟังก์ชัน
        tab_list = mybot.get_all_sheet_names(Json_path, Sheet_name)

        if not tab_list:
            print("❌ ไม่พบ Tab ในไฟล์นี้")
            return
        
        full_output_path = os.path.join(current_dir, output_filename)
        print(f"Saving to: {full_output_path}")

        mf.save_to_txt_dict(tab_list,file_name,full_output_path)

    except Exception as e:
        print(f"\n❌ Error log : {e}")

def get_worksheet_from_file(file_name):
    
    mf = MyFileLib()
    
    # สร้าง Path เต็ม
    full_path = os.path.join(current_dir, file_name)
    
    print(f"--- Reading from: {file_name} ---")
    
    # เลือกใช้วิธีอ่าน (สมมติว่าเป็นไฟล์รายชื่อ Tab ที่เราเพิ่ง Save)
    # ใช้วิธีที่ 1 (read_txt_lines) ก็พอ เพราะข้อมูลเป็นแค่ชื่อ
    data = mf.read_id_value_pair(full_path)

    if not data:
        print("⚠️ ไม่พบข้อมูล หรือไฟล์ว่างเปล่า")
        return [] # ส่ง List ว่างกลับไป
    
    if data:
        #print(f"✅ อ่านสำเร็จ! พบข้อมูล {len(data)} บรรทัด:")
        #for i, item in enumerate(data, 1):
        #    print(f"{i}. {item}")
    
        return data

    else:
        print("ว่างเปล่า หรือ หาไฟล์ไม่เจอ")




# --- เริ่มทำงาน ---

# --- recived worksheet from sheets using API and save to txt ---    
#    get_worksheet_and_save_file(Json_path,Sheet_name,'Oxford 3000 Sorted','output_filename')


# --- read worksheet from file ---
def export_to_quizlet():
    ms = MyFileLib()
    mybot = MysheetLib()    
    
    my_result_data = get_worksheet_from_file(output_filename)   
    
    list_data_out = []
    list_data = []
    
    for name_worksheers in range (21,28):
        

        list_data = mybot.get_google_sheet_data(Json_path,Sheet_name,my_result_data[name_worksheers])

        for each_word in range (0,len(list_data)):
            list_data_out.append(str(list_data[each_word]['No.']) + '. ' + list_data[each_word]['Word'] + '    ' + list_data[each_word]['Meaning']+ ' ('+list_data[each_word]['POS']+')')
        
        ms.save_to_txt(list_data_out,f"{my_result_data[name_worksheers]}.txt")
        list_data_out.clear()

if __name__ == "__main__":
    export_to_quizlet()