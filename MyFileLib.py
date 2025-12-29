import  os
import  sys
import ast


class   MyFileLib:

    # ---------------------------------------------------------------------
    # ฟังก์ชันสำหรับบันทึกข้อมูลลงไฟล์ .txt
    def save_to_txt(self, data_list, filename):
        """
        รับข้อมูล (List) และ ชื่อไฟล์ปลายทาง (.txt)
        แล้วบันทึกลงเครื่อง
        """
        try:
            # 1. เปิดไฟล์ (w = เขียนทับ, a = เขียนต่อท้าย)
            # encoding='utf-8' สำคัญมาก! เพื่อให้อ่านภาษาไทยออก
            with open(filename, 'w', encoding='utf-8') as f:
                
                # 2. วนลูปเขียนข้อมูลทีละบรรทัด
                for row in data_list:
                    # แปลงข้อมูลเป็นข้อความ (String) แล้วเติม \n เพื่อขึ้นบรรทัดใหม่
                    f.write(str(row) + "\n")
            
            print(f"✅ บันทึกไฟล์สำเร็จ: {filename}")
            return True

        except Exception as e:
            print(f"❌ บันทึกไฟล์ไม่สำเร็จ: {e}")
            return False
        

    # ---------------------------------------------------------------------
    # ฟังก์ชันสำหรับบันทึกข้อมูลลงไฟล์ .txt แบบ dirctionaly
    def save_to_txt_dict(self, data_list, sheet_name,txt_output_name):
        """
        รับข้อมูล (List) และ ชื่อไฟล์ปลายทาง (.txt)
        แล้วบันทึกลงเครื่อง
        """
        try:

            limit = len(data_list)

            # 2. สร้าง Dictionary Key ตัวเลข (1-36)
            numbered_dict = {}
            for index, row in enumerate(data_list, start=1):
                numbered_dict[index] = row
                if index == limit:
                    break
            
            # 3. บันทึกลงไฟล์ .txt
            # จะบันทึกแบบบรรทัดละ 1 key เพื่อให้อ่านง่าย
            with open(txt_output_name, 'w', encoding='utf-8') as f:
                # เขียน Header บอกหน่อยว่าไฟล์นี้คืออะไร (Optional)
                f.write(f"# Data from {sheet_name} (Total: {len(numbered_dict)})\n")
                
                for key, value in numbered_dict.items():
                    # เขียนลงไฟล์ เช่น: 1: {'Term': 'Hi', 'Def': 'สวัสดี'}
                    f.write(f"{key}: {value}\n")
            
            print(f"✅ บันทึกสำเร็จ! ไฟล์อยู่ที่: {txt_output_name}")
            return numbered_dict

        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            return {}
        

    # -----------------------------------------------------------
    # แบบที่ 1: อ่านไฟล์ธรรมดา (อ่านทีละบรรทัด)
    # เหมาะกับ: ไฟล์รายชื่อ, Log, หรือไฟล์ Text ทั่วไป
    def read_txt_lines(self, filename):
        try:
            results = []
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    # .strip() ตัดช่องว่างหัวท้ายและ \n ออก
                    clean_line = line.strip()
                    if clean_line: 
                        results.append(clean_line)
            return results
        except FileNotFoundError:
            print(f"❌ หาไฟล์ไม่เจอ: {filename}")
            return []
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return []


    # -----------------------------------------------------------
    # แบบที่ 3: อ่านไฟล์ Format "ID: ข้อความ"
    # เหมาะกับบรรทัดแบบ: "1: 1. PEOPLE & RELATIONSHIPS"
    def read_id_value_pair(self, filename):
        result_dict = {}
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    clean_line = line.strip()
                    
                    # เช็คว่าบรรทัดนี้มีเครื่องหมาย : หรือไม่
                    if ':' in clean_line:
                        # 1. ผ่าข้อความออกจากกัน (ผ่าแค่ครั้งแรกที่เจอ : เพื่อความชัวร์)
                        # เช่น "1: Hello:World" -> จะได้ ["1", " Hello:World"]
                        parts = clean_line.split(':', 1)
                        
                        if len(parts) == 2:
                            key_str = parts[0].strip()   # ได้ "1"
                            val_str = parts[1].strip()   # ได้ "1. PEOPLE..."
                            
                            # 2. พยายามแปลง Key เป็นตัวเลข
                            if key_str.isdigit():
                                key = int(key_str)       # แปลง "1" เป็นเลข 1
                                result_dict[key] = val_str
                            else:
                                # ถ้าข้างหน้าไม่ใช่ตัวเลข ก็เก็บเป็น text เหมือนเดิม
                                result_dict[key_str] = val_str
                                
            return result_dict # ส่ง Dict กลับไป

        except Exception as e:
            print(f"❌ อ่านไฟล์ไม่สำเร็จ: {e}")
            return {}