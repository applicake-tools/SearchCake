import os
import platform
import searchcake.libcreateWF as libcreateWF
import pandas as pd
import pepidentWFconfig as pwconf
import ntpath
import datetime


def run(files, db_path, work_dir):
    pwconf.remove_ini_log()
    tmp = pwconf.setup_general() + pwconf.setup_search()
    if platform.system() == 'Linux':
        tmp += pwconf.setup_linux()
    else:
        tmp += pwconf.setup_windows()
    print(tmp)
    pwconf.write_ini(tmp)
    pwconf.peptidesearch_overwriteInfo({'INPUT': "input.ini",
                                        'MZXML': files,
                                        'DBASE': pwconf.getDB(),
                                        'OUTPUT': 'output.ini',
                                        'JOB_ID': work_dir,
                                        'DB_PATH': db_path})

    libcreateWF.run_libcreate_withNetMHC2_WF(nrthreads=4)


def processAllFiles(all_mz_xmls,work_dir):
    db_path = "{}/SysteMHC_Data/annotation/cleanedTable_id.csv".format(
        os.environ.get('SYSTEMHC'))
    df = pd.read_csv(db_path)

    filesIds = df['FileName']
    res = list()
    for i in filesIds:
        res += [x for x in all_mz_xmls if ntpath.basename(x) == i]
    run(res, db_path,work_dir)


if __name__ == '__main__':
    res = os.environ.get('SYSTEMHC')

    if res == None:
        print "SYSTEMHC not set"
        exit(1)
    files = pwconf.getMzXMLFiles("/mnt/Systemhc/Data/PXD001872/")
    now = datetime.datetime.now()
    processAllFiles(files, 'eLifeWorkflow' + str(now.hour) + str(now.minute))


# pipeline_printout_graph ('flowchart.png','png',[copy2dropbox],no_key_legend = False) #svg
