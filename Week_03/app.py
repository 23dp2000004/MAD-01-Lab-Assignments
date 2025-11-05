import sys
from jinja2 import Template
import matplotlib.pyplot as plt

cli_args = sys.argv  #['filename', 'flag', 'id']

#Templates
#templates start

student_template = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Data</title>
</head>
<body>
    <h1>Student Details</h1>                     
     <table border="1px">
        <thead>
            <tr>
                <th>Student id</th>
                <th>Course id</th>
                <th>Marks</th>
            </tr>
        </thead>
        <tbody>
            {% for row in StudentData %}
            <tr>
                <td>{{ row['sid'] }}</td>
                <td>{{ row['cid'] }}</td>
                <td>{{ row['marks'] }}</td>
            </tr>
            {% endfor %}
        </tbody>
        <tfoot>
            <tr>
                <td colspan="2">Total Marks</td>
                <td>{{TotalMarks}}</td>
            </tr>
        </tfoot>
     </table>
</body>
</html>
""")


course_template = Template ("""
 <!DOCTYPE html>
 <html lang="en">
 <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Course Data</title>
 </head>
 <body>
    <h1>Course Details</h1>
    
    
    <table border="1px">
        <thead>
            <tr>
                <th>Average Marks</th>
                <th>Maximum Marks</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{{AverageMarks}}</td>
                <td>{{MaximumMarks}}</td>
            </tr>
        </tbody>
    </table>

     <img src="{{URL_graph}}" alt="image of a histogram" width="250" height="250">
 </body>
 </html>
""")


error_template = Template("""
 <!DOCTYPE html>
 <html lang="en">
 <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Something Went Wrong</title>
 </head>
 <body>
    <h1>Wrong Inputs</h1>
    <p>Something went wrong</p>
 </body>
 </html>
""")
#templates end



file = open('data.csv') #relative path
lines = file.readlines()[1:] #the header row will be ignored
file.close()

#Error Message
if ((len(cli_args) != 3) or cli_args[1] not in ('-s' ,'-c')):
    f = open('output.html', 'w')
    f.write(error_template.render())
    f.close()
    #print("Something went wrong")

else:
    if cli_args[1] == '-s':
        
        cli_sid = cli_args[2]
        total_marks = 0
        student_data = []         #[{'sid':1001, 'cid':2001, 'marks':56}, ...]

        for line in lines:
            #print(line)
            #print(repr(line), type(line))

            file_sid, file_cid, file_marks = line.split(', ') #split will result in a list of strings 
            file_marks = int(file_marks)

            if file_sid == cli_sid:
                row = {'sid': file_sid, 'cid': file_cid, 'marks': file_marks}
                student_data.append(row)

                total_marks += file_marks


        #Error Message
        if not student_data: #if student_data is empty
            f = open('output.html', 'w')
            f.write(error_template.render())
            f.close()
            sys.exit()

        output = student_template.render(
            StudentData = student_data,
            TotalMarks = total_marks
            )
        
        f = open('output.html', 'w')
        f.write(output)
        f.close()

    elif cli_args[1] == '-c':
        cli_cid = cli_args[2]
        total_marks = 0         #to compute avg
        count = 0               #to compute avg
        max_marks = 0
        marks_list = [] 
          
        for line in lines:

            file_sid, file_cid, file_marks = line.split(', ')
            file_marks = int(file_marks)

            if file_cid == cli_cid:
                total_marks += file_marks
                count += 1
                max_marks = max(file_marks, max_marks) 
                marks_list.append(file_marks)


        #Error Message
        if not marks_list: #if marks_list is empty
            f = open('output.html', 'w')
            f.write(error_template.render())
            f.close()
            sys.exit()

        #Histogram plot
        plt.hist(marks_list, bins=10) #hist will generate the histogram
        plt.xlabel("Marks")
        plt.ylabel("Frequency")
        plt.savefig("histogram.png")
        #plt.show()
        plt.close()

        output = course_template.render(
            AverageMarks = total_marks/count,
            MaximumMarks = max_marks,
            URL_graph = "histogram.png"
            )
        
        f = open('output.html', 'w')
        f.write(output)
        f.close()



    