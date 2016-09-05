from lxml import etree
import re
import csv


def parsePepXMLProbToErroMapping(file,outfile):
    header_set = False
    f = open(outfile, 'wb')
    writer = csv.writer(f, delimiter='\t')
    for event, elem in etree.iterparse(file):

        if event == 'end' and re.search("error_point$", elem.tag):
            result = {}
            result['min_prob'] = elem.get("min_prob")
            result['error'] = elem.get("error")
            result['num_incorr'] = elem.get("num_incorr")
            result['num_corr'] = elem.get("num_corr")
            if not header_set:
                writer.writerow(result.keys())
                header_set = True
            writer.writerow(result.values())
        if event == 'end' and re.search("roc_error_data$", elem.tag):
            print(elem.tag)
            f.close()
            return


if __name__ == "__main__":
    file = "/mnt/Systemhc/Data/process2/marcillam_160207_marcilla_Spain_C1R_1/InterProphet/iprophet.pep.xml"
    outfile = "dumm.txt"
    parsePepXMLProbToErroMapping(file, outfile)



