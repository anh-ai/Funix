#import thư viện 
import os
import pandas as pd
import numpy as np

def inputName(): #yêu cầu nhập tên file và thêm đuôi .txt
    mDir="Data Files/"
    fRun=True
    # while fRun: # có thể đọc đến khi nào file tồn tại thì dừng.
    if fRun:
        #kiểm tra xem người dung có nhập đúng dạng tên file 
        print("Which grade file do you want to open (Ex: class1 or class1.txt) or press Ctr_C to exit program ?")
        file_name = input()
        

        #chuan hoa ten file ma người dùng nhập vào thành đuôi .txt theo tên file dữ liệu trong Data Files
        # vd class1 -> class1.txt
        # nếu user nhập class1.txt thì giữ nguyên
        for file in os.listdir(mDir):
            if file_name  == file :
                return file_name
        
        file_name = file_name + ".txt" 
        # if exists(f"{mDir}{file_name}"):
        #     fRun=False
    return file_name 

def openGradeFile(file_name): #mở file đáp án của sinh viên và trả lại nội dung
    content = ''
    #mở file và bắt lỗi
    try:
        with open("./Data Files/" +file_name ,"r") as grade_file:
            print("Successfully open " + file_name)
            content = grade_file.read()
    
    except: 
        print("Sorry the file name " + file_name + " is not exist\n")
        print("Make sure your file have the form of classN:\n" 
             "For example: class1, class2, class3,...\n"
             "If you do, maybe your class is not in the DataFiles folder")
    
    return content #trả lại nội dung file được mở ở kiểu string


def analyzeInvalid(content,file_name): #Phân tich file điểm số xem có bn invalid line
    
    #Cắt chuỗi content ở dấu xuống dòng thành list các chuỗi ID và đáp an
    content = content.split('\n')
    valid_content = content[:]
    print('*'*4 + 'ANALYZING' + '*'*4 +'\n')
    error = 0 #biến đếm số invalid line trong file txt

    #Xét từng chuỗi ID và đáp án của học sinh
    for paper_work in content:
        answer = paper_work.split(',')
        #kiểm tra định dạng mã số sinh viên
        if ((answer[0][0] != 'N') or (len(answer[0]) != 9)):
            print("Invalid line of data: N# is invalid")
            print(paper_work + '\n')
            error += 1
            valid_content.remove(paper_work)
        elif (answer[0][1:8].isdigit() == False):
            print("Invalid line of data: N# is invalid")
            print(paper_work + '\n')
            error += 1
            valid_content.remove(paper_work)
    #kiểm tra số lượng câu trả lời
        elif (len(answer) != 26):
            print("Invalid line of data: does not contain exactly 26 values:")
            print(paper_work + '\n')
            error += 1
            valid_content.remove(paper_work)
    
    
    #in thông báo
    if(error == 0):
        print("No errors found!\n")
        print('*'*4 + 'REPORT' + '*'*4 + '\n')
        print('Total valid lines of data: ' + str(len(content)) + '\n')
        print('Total invalid lines of data: 0\n')
        print('Enter a class to grade: ' + file_name + '\n') 
    else:
        print('*'*4 + 'REPORT' + '*'*4 + '\n')
        print('Total valid lines of data: ' + str(len(content) - error) + '\n')
        print('Total invalid lines of data: ' + str(error))
    
    return valid_content

def classgradeDescribe(valid_content): #Phân tích mean,mã,min,med và chấm điểm
    
    #Cắt chuỗi answer key thành list các đáp án đúng
    answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
    answer_key = answer_key.split(',')

    #Từ điển chứa ID và đáp án
    grade_dict = {'Student ID' : [], 'Grade' : []}

    #Xét từng chuỗi ID và đáp án trong content
    for paper_work in valid_content:
        point = 0
        answer = paper_work.split(',') #cắt chuỗi thành list ID và đáp án
        answer_noID = answer[:] #Tạo clone của list answer
        answer_noID.pop(0) #Loại bỏ ID của sinh viên ra khỏi list answer_noID
        
        #So sánh câu trả lời của sinh viên trong answer_noID với đáp án đúng trong key
        #Tính điểm
        for student_ans, correct_ans in zip(answer_noID,answer_key):
            if student_ans == correct_ans:
                point += 4
            elif student_ans == '':
                pass
            elif (student_ans != correct_ans) and (student_ans != ''):
                point -= 1
        #Đưa ID và điểm tương ứng vào từ điển
        grade_dict['Student ID'].append(answer[0])
        grade_dict['Grade'].append(point)
    #Chuyển từ điển thành DataFrame 
    grade_table = pd.DataFrame(grade_dict)
    #In mean,max,min,range,med của điểm số
    print(f"Mean (Average) score of the class: {round(grade_table['Grade'].mean(),2)} \n")
    print(f"Highest score: {grade_table['Grade'].max()}\n")
    print(f"Lowest score: {grade_table['Grade'].min()}\n")
    print(f"Range of score: {grade_table['Grade'].max() - grade_table['Grade'].min()}\n")
    print(f"Median Score: {grade_table['Grade'].median()}\n")

    return grade_table #trả lại bảng điểm kiểu DataFrame

def saveGradefile(file_name,grade_table): #lưu file điểm số sau khi chấm

    save_name = file_name[0:file_name.rfind('.')] + "_grades" + \
                file_name[file_name.rfind('.'):]  
    #lưu file vào thư mục hiện hành và bắt lỗi                        
    try:
        grade_table.to_csv(save_name.lower(), sep='\t', index=False)
        print(f"A class grade file named :{save_name.lower()} is created in current folder\n"
            "Please go to your current folder to view it \n")
    except:
        print(f"Cannot save {save_name} due to an unexpected problems")

#hàm main()
def main():

    try:
        file_name = inputName() #yêu cầu nhập tên file
        content = openGradeFile(file_name) #mở file txt lưu nội dung vào biến content
        
        #chấm điểm và phân tích thống kê, lưu bảng điểm vào biến grade_table
        grade_table = classgradeDescribe(analyzeInvalid(content,file_name)) 
    except:
        print("Cannot analyze your grade file. Please try again")
    
    try:    
        #lưu file chấm điểm thư mục hiện hành                                 
        saveGradefile(file_name,grade_table)
    except:
        print("Cannot save your grade file due to unexpected problems")

if __name__ == "__main__":
    main()

