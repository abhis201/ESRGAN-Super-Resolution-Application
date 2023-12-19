import os

def rename(path):

    for count, filename in enumerate(os.listdir(path)): 
        dst =filename.split("_")[0] + "_" + filename.split(".")[0].split("_")[1].zfill(4) + ".png"
        src = path + "/" +  filename 
        dst = path + "/" + dst
        os.rename(src, dst) 


rename('lr_test')
rename('hr_test')
