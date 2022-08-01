#!/usr/bin/python

import sys
import shutil
import os

import zipfile

import jaydebeapi
import jpype


#rename files in folder
def db_rename(db_folder, name, type):
    for root, dirs, files in os.walk(db_folder):
        for file in files:
            org_file = file
            new_file = file
            if type == 'file2name':
                org_file = db_folder + file
                new_file = db_folder + name + '.' + file
            elif type == 'name2file':
                org_file = db_folder + file
                nf = file.replace(name + '.','')
                new_file = db_folder + nf
            else:
                print 'Error in db_rename, bad type'
                sys.exit()
            #endif
            shutil.move(org_file, new_file)
        #endfor
    #endfor
#enddef


#copy the odb to tmp dir and rename it zip
path = '/home/tad/Desktop/aiken_tax_pages/'
tmpdir = path + 'tmp/'

if not os.path.exists(tmpdir):
    os.makedirs(tmpdir)
#endif

name = 'delinquient_aiken_data'
odb  = path + name + '.odb'
zip  = path + 'tmp/' + name + '.zip'
db_name = path + 'tmp/' + name + '/'

shutil.copyfile(odb, zip)

#unzip it
zip_ref = zipfile.ZipFile(zip)
zip_ref.extractall(db_name) #tmpdir+name)
zip_ref.close()

#delete the org zip?
os.remove(zip)

#go to database folder and rename files to odb_name.X
db_folder = db_name + 'database/'
db_rename(db_folder,name,'file2name')
db = db_folder + name

#do database stuff
classpath = ('/usr/lib/jvm/java-6-openjdk-amd64/jre/lib/'
             ':/usr/share/java/hsqldb.jar:.')
jvm_path  = '/usr/lib/jvm/java-6-openjdk-amd64/jre/lib/amd64/server/libjvm.so'
jpype.startJVM(jvm_path, '-Djava.class.path=%s' % classpath)
#jpype.java.lang.System.out.println("hello world")

conn = jaydebeapi.connect('org.hsqldb.jdbcDriver', 
                          'jdbc:hsqldb:file:'+db,
                          'SA', '')
cur = conn.cursor()

str = 'select * from \"delinquient_2013\"'
cur.execute(str)
a_result = cur.fetchall()

print len(a_result)
#for loc in a_result:
#    if loc[1] == "PUBLIC":
#    print loc[1]
    #endif
#endfor
cur.execute("SHUTDOWN")
cur.close()
conn.close()

db_folder = db_name + 'database/'

#rename files to X
db_rename(db_folder,name,'name2file')

#zip it
zip_ref = zipfile.ZipFile(zip, "w", zipfile.ZIP_DEFLATED)
for root, dirs, files in os.walk(db_name):
    for file in files:
        zip_ref.write(os.path.join(root, file))
    #endfor
#endfor
zip_ref.close()

#delete the tmp unzipped db
shutil.rmtree(db_name)

#rename it odb
odb2 = path + name + '2.odb'
shutil.move(zip, odb2)


#jpype.shutdownJVM()
sys.exit()
