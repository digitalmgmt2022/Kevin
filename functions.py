import os,json

def setcompleted_jobs(title,jobdescriptionurl,location,id):
    """ This Function is used for not repeting publishing jobs
    """
    filesDir=os.listdir()
    if "CompletedJobs.txt" in filesDir:
        datalog=open("CompletedJobs.txt","a")
    else:
        datalog=open("CompletedJobs.txt","w")
        datalog.write("Title|Jobdescription|Location|ID\n")
        datalog.close()
        datalog=open("CompletedJobs.txt","a")
    
    datalog.write(title+"|"+jobdescriptionurl+"|"+location+"|"+id+"\n")
    datalog.close()

def idcompleted():
    """This function is used for getting all ID completed in CompletedJobs.txt file
    """
    filesDir=os.listdir()
    ids=[]
    if "CompletedJobs.txt" in filesDir:
        lines=open("CompletedJobs.txt").readlines()
        for line in lines:
            ids.append(line.split("|")[3].replace("\n",""))
        return ids
    else:
        return ids