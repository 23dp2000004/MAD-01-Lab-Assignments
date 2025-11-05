from flask import Flask, request, render_template
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend suitable for servers
from matplotlib import pyplot as plt

with open('data (1).csv') as file: #data (1).csv for local, but data for submission
    file_data = file.readlines()[1:] #excludes the header from the csv file

#Histogram plot
def image_creator(marks_list):
    plt.hist(marks_list, bins =10) #hist will generate the histogram
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    plt.savefig("static/image.png")
    plt.close()
    #plt.show()



app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template('index.html')

    elif request.method == "POST":
        form_data = request.form
        #return form_data

        if form_data["ID"] == "student_id":
            #return "selected s_id"

            _sid = form_data["id_value"] #sid give in form
            student_data = [] #list of dictionaries, each dict = entry of student
            total_marks = 0

            for row in file_data:
                sid, cid, marks = row.strip().split(", ")
                marks = int(marks)

        
                if sid == _sid: #if student exists, get the details.
                    entry = {"sid": sid, "cid": cid, "marks": marks}
                    student_data.append(entry)
                    total_marks += marks 
            
            if student_data: ##if student_data list is not empty
                #return student_data #change this to redirect to the html page
                return render_template(
                    "StudentData.html", 
                    data = student_data, #data is variable in the html file, in the for loop
                    total = total_marks  #total is variable from the html file
                    )
            else: 
                #return "error" #change this to redirect to the html page
                return render_template("ErrorMesg.html")

        elif form_data["ID"] == "course_id":
            #return "selected c_id"
            _cid = form_data["id_value"] #sid give in form
            max_marks = 0
            marks_data = [] #will be used to calculate avg marks
            count = 0  #will be used to calculate avd marks
            average_marks = None

            for row in file_data:
                sid, cid, marks = row.strip().split(", ")
                marks = int(marks)

        
                if cid == _cid: #if course exists, get the details.
                    marks_data.append(marks)
                    count += 1
                    max_marks = max(marks, max_marks)
                
            if marks_data: #if marks_data list is not empty
                average_marks = sum(marks_data) / count
                image_creator(marks_list = marks_data)
                #return marks_data #change this to redirect to the html page
                return render_template(
                    "CourseData.html",
                    avg = average_marks,
                    maxi = max_marks
                )
            
            else: 
                #return "error" #change this to redirect to the html page
                return render_template("ErrorMesg.html")
            
            
            

if __name__ == "__main__":
    app.run(debug=True)

