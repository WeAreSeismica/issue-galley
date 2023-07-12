 
import os
import pandas as pd
from edstats.api import OJSSession
from ojssecret import username, password
from urllib.request import urlretrieve
import shutil
import re
import json
from bs4 import BeautifulSoup
import pypdf
from PIL import Image
import subprocess
from argparse import ArgumentParser

# Set local info
parser = ArgumentParser()
parser.add_argument('--volume','-v',type=int,help='issue volume')
parser.add_argument('--number','-n',type=int,help='issue number')
parser.add_argument('--odir','-o',type=str,help='path to output issue galleys')
parser.add_argument('--tex', action='store_true',help='run LuaTeX (default) ')
parser.add_argument('--no-tex', dest='tex', action='store_false', help='Manually run LuaTeX via a separate editor (False, use if you want to manually edit the .tex)')
parser.set_defaults(tex=True)

args = parser.parse_args()
volume = args.volume
if volume == None:
    volume = input('Enter Issue volume: ') or 1
number = args.number
if number == None:
    number = input('Enter Issue number: ') or 1
issuedir = args.odir
if issuedir == None:    
    odir = './issues-galleys/'
    issuedir = input('Enter path to output issue galleys, or use %s: ' % odir) or odir 
latex = args.tex

if not os.path.exists(issuedir):
    os.makedirs(issuedir)

latexdir = './issue_template/'
    
# Create the OJSSession (that keeps cookies/session info)
s = OJSSession()
s.connect(username=username, password=password)

issue, issueID = s.get_issue_from_volnum(volume=volume, number=number)

sections, articles, participants = s.get_issue_byID(issueID)

# get stages for each article, and participants for each stage
stages = {}
participantsBystage = {}

for i in range(len(articles)):
    articleID = articles['id'][i]
    stages[articleID] = s.get_stages_byID(articleID)
    participantsBystage[articleID] = []

    for st in range(len(stages[articleID])):
        parts = s.get_participants_byStage(articleID, stages[articleID]['id'][st])
        participantsBystage[articleID].append( parts )

# create folder for the issue
newdir = issuedir+'v{}n{}'.format(volume, number)
if not os.path.exists(newdir):
    os.makedirs(newdir)

# download galleys for all articles of issue
# XML is used to retrieve Production editors, Reviewer and Translators information
for i in range(len(articles)):
    try:
        articleID = articles['id'][i]
        pdfID = articles['publications'][i][0]['galleys'][0]['id']
        fileID = articles['publications'][i][0]['galleys'][0]['file']['id']
        pdf_url = "https://seismica.library.mcgill.ca/article/download/{}/{}/{}".format(articleID, pdfID, fileID)
        oname = newdir+'/'+str(articleID)+'.pdf'
        if not os.path.isfile(oname):
            urlretrieve(pdf_url, oname)

        xmlID = articles['publications'][i][0]['galleys'][1]['id']
        fileID = articles['publications'][i][0]['galleys'][1]['file']['id']
        xml_url = "https://seismica.library.mcgill.ca/article/download/{}/{}/{}".format(articleID, xmlID, fileID)
        oname = newdir+'/'+str(articleID)+'.xml'
        if not os.path.isfile(oname):
            urlretrieve(xml_url, oname)
        
    except IndexError:
        articleID = articles['id'][i]
        articles = articles.drop(i).copy()
        print('Article ID {} does not have published galleys'.format(articleID))
articles = articles.reset_index() # in case unpublished article has been dropped


# get list of volunteers by role
proded = {}
handed = {}
copyed = {}
media = {}
reviewers = {}
translators = {}

for i in range(len(articles)):
    articleID = articles['id'][i]

    for p in range(len(participants[articleID])):
        parti = participants[articleID].loc[p]
        if 'Copyeditor' in [x['name']['en_US'] for x in parti['groups']]:
            nm = parti['fullName'].title()
            if nm not in copyed.keys():
                copyed[nm] = parti['orcid']
        elif 'Media + Branding' in [x['name']['en_US'] for x in parti['groups']]:
            nm = parti['fullName'].title()
            if nm not in media.keys():
                media[nm] = parti['orcid']
        elif 'Handling editor' in [x['name']['en_US'] for x in parti['groups']]:
            nm = parti['fullName'].title()
            if nm not in handed.keys():
                handed[nm] = parti['orcid']

# get proded, reviewers and translators from XML metadata
for i in range(len(articles)):
    articleID = articles['id'][i]
    try:
        with open(newdir+'/'+str(articleID)+'.xml') as fi:
            xml = fi.read()
        soup = BeautifulSoup(xml, 'xml')

        for p in soup.find_all('contrib', attrs={'contrib-type': "reviewer"}):
            gn = p.find('given-names').text
            sn = p.find('surname').text
            if not any(sn in key for key in reviewers):
                if 'anonymous' not in gn+' '+sn:
                    reviewers[gn+' '+sn] = s.get_users_orcid(gn, sn) # try to find ORCID in OJS database

        for p in soup.find_all('contrib', attrs={'contrib-type': "translator"}):
            gn = p.find('given-names').text
            sn = p.find('surname').text
            if not any(sn in key for key in translators):
                translators[gn + ' ' + sn] = s.get_users_orcid(gn, sn)  # try to find ORCID in OJS database

        for p in soup.find_all('contrib', attrs={'contrib-type': "editor"}):
            if 'Production Editor' in p.find('role'):
                gn = p.find('given-names').text
                sn = p.find('surname').text
                if not any(sn in key for key in proded):
                    proded[gn + ' ' + sn] = s.get_users_orcid(gn, sn)  # try to find ORCID in OJS database

    except UnicodeDecodeError:
        print('XML file for article ID {} not found or incorrect\n'.format(articleID))

re_txt = [list(reviewers)[i]+"\orcid{"+list(reviewers.values())[i].replace('https://orcid.org/','')+'}' for i in range(len(reviewers))]
re_txt = ', '.join(re_txt)
tr_txt = [list(translators)[i]+"\orcid{"+list(translators.values())[i].replace('https://orcid.org/','')+'}' for i in range(len(translators))]
tr_txt = ', '.join(tr_txt)

# get issue additional text
caption = BeautifulSoup(issue['description.en_US'].values[0], 'lxml').text
title = BeautifulSoup(issue['title.en_US'].values[0], 'lxml').text

# clean caption
summary, caption = caption.split('Cover caption:')

# fill in imprint TeX file
imprintFiname = newdir+'/imprint_{}.tex'.format(issueID)
shutil.copy(latexdir+'imprint_template.tex', imprintFiname)
shutil.copy(latexdir+'seismica_cover.cls', newdir+'/seismica_cover.cls')
shutil.copy(latexdir+'banner_imprint.png', newdir+'/banner_imprint.png')

pr_txt = [list(proded)[i]+"\orcid{"+list(proded.values())[i].replace('https://orcid.org/','')+'}' for i in range(len(proded))]
pr_txt = ', '.join(pr_txt)
he_txt = [list(handed)[i]+"\orcid{"+list(handed.values())[i].replace('https://orcid.org/','')+'}' for i in range(len(handed))]
he_txt = ', '.join(he_txt)
cp_txt = [list(copyed)[i]+"\orcid{"+list(copyed.values())[i].replace('https://orcid.org/','')+'}' for i in range(len(copyed))]
cp_txt = ', '.join(cp_txt)
mb_txt = [list(media)[i]+"\orcid{"+list(media.values())[i].replace('https://orcid.org/','')+'}' for i in range(len(media))]
mb_txt = ', '.join(mb_txt)

with open(imprintFiname, 'r') as fi:
    tex = fi.readlines()

with open(imprintFiname, "w", encoding='utf-8') as fi:
    for line in tex:
        fi.write(line)
        if 'documentclass' in line:
            fi.write("\\thevolume{{{}}}".format( issue['volume'].values[0] ))
            fi.write("\\thenumber{{{}}}".format( issue['number'].values[0] ))
            fi.write("\\theyear{{{}}}".format( issue['year'].values[0] ))
            if len(title) != 0:
                fi.write("\\subtitle{{{}}}".format( title ))

        if 'Production Editors' in line:
            fi.write(pr_txt)
        elif 'Handling Editors' in line:
            fi.write(he_txt)
        elif 'Copy' in line:
            fi.write(cp_txt)
        elif 'Media' in line:
            fi.write(mb_txt)
        elif 'Reviewer' in line:
            fi.write(re_txt)
        elif 'Translator' in line and len(tr_txt)>3:
            fi.write('\\paragraph{Translators}\n')
            fi.write(tr_txt)
        elif 'Cover Caption' in line:
            fi.write(caption)
        elif 'if summary' in line and len(summary) > 10:
            fi.write('\\begin{summary}{}\n')
            fi.write(summary)
            fi.write('\\end{summary}\n')

#---- make TOC
tocFiname = newdir+'/toc_{}.tex'.format(issueID)
shutil.copy(latexdir+'toc_template.tex', tocFiname)

txt_by_sections = []
for i in range(len(sections)):
    sec_txt = '\\section*{{{}}}'.format(sections['title'][i]['en_US'])

    ar_txt = []
    for ar in range(len(articles['publications'])):
        if articles['publications'][ar][0]['sectionId'] == sections['id'][i]:
            ar_title = articles['publications'][ar][0]['fullTitle']['en_US']
            ar_auth = articles['publications'][ar][0]['authorsStringShort']
            ar_doi = 'https://doi.org/'+articles['publications'][ar][0]['pub-id::doi']
            ar_txt.append( '\\insertarticle{{{title}}}{{{auth}}}{{{doi}}}'.format(title=ar_title, auth=ar_auth, doi=ar_doi))
    full_txt = sec_txt + ' \n\n'.join(ar_txt)
    txt_by_sections.append(full_txt)

with open(tocFiname, 'r') as fi:
    tex = fi.readlines()

with open(tocFiname, "w", encoding='utf-8') as fi:
    for line in tex:
        fi.write(line)
        if 'documentclass' in line:
            fi.write("\\thevolume{{{}}}".format( issue['volume'].values[0] ))
            fi.write("\\thenumber{{{}}}".format( issue['number'].values[0] ))
            fi.write("\\theyear{{{}}}".format( issue['year'].values[0] ))
            fi.write("\\subtitle{{Table of Contents}}")

        if 'insert below' in line:
            for i in range(len(txt_by_sections)):
                fi.write(txt_by_sections[i])

# run LATEX
if latex is True:
    cmd = """
    cd {dir}
    lualatex -synctex=1 -interaction=nonstopmode -shell-escape "{fil}".tex
    """.format(dir=newdir, fil=tocFiname.split('/')[-1].replace('.tex',''))
    subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL)

    cmd = """
    cd {dir}
    lualatex -synctex=1 -interaction=nonstopmode -shell-escape "{fil}".tex
    """.format(dir=newdir, fil=imprintFiname.split('/')[-1].replace('.tex',''))
    subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL)
else:
    print('\nNeed to run LuaTeX to produce PDFs!\n')
    
# download cover from website
cover_url = issue['coverImageUrl.en_US'].values[0]
coverFiname = newdir+'/cover_'+str(issueID)+'.png'
if not os.path.isfile(coverFiname):
    urlretrieve(cover_url, coverFiname)
if not os.path.isfile(coverFiname.replace('.png','.pdf')):
    png = Image.open(coverFiname)
    png.load()
    background = Image.new("RGB", png.size, (255, 255, 255))
    background.paste(png, mask=png.split()[3])
    background.save(coverFiname.replace('.png','.pdf'),"PDF",resolution=800)

# merge all PDFs for Full issue
merger = pypdf.PdfMerger()
merger.append(coverFiname.replace('.png','.pdf'))
merger.append(imprintFiname.replace('.tex','.pdf'))
merger.append(tocFiname.replace('.tex','.pdf'))

# Sort articles by section to follow TOC order
for i in range(len(sections)):
    for ar in range(len(articles['publications'])):
        if articles['publications'][ar][0]['sectionId'] == sections['id'][i]:
                articleID = articles['id'][ar]
                pdf = newdir+'/'+str(articleID)+'.pdf'
                merger.append(pdf)

fullName = newdir+"/seismica_v{}n{}_hr.pdf".format(volume, number)
coverName = newdir+"/seismica_v{}n{}_info_hr.pdf".format(volume, number)
merger.write(fullName)
merger.close()

# merge all PDFs for Issue Information file
merger = pypdf.PdfMerger()
merger.append(coverFiname.replace('.png','.pdf'))
merger.append(imprintFiname.replace('.tex','.pdf'))
merger.append(tocFiname.replace('.tex','.pdf'))
merger.write(coverName)
merger.close()

# Decrease final PDF size
cmd = """
cd {dir}
gs -q -dNOPAUSE -dBATCH -dSAFER -dPDFA=2 -dPDFACompatibilityPolicy=1 -dSimulateOverprint=true -sDEVICE=pdfwrite -dCompatibilityLevel=1.3 -dPDFSETTINGS=/screen -dEmbedAllFonts=true -dSubsetFonts=true -dAutoRotatePages=/None -dColorImageDownsampleType=/Bicubic -dColorImageResolution=200 -dGrayImageDownsampleType=/Bicubic -dGrayImageResolution=150 -dMonoImageDownsampleType=/Bicubic -dMonoImageResolution=200 -sOutputFile={outfi} {infi}
""".format(dir=newdir, outfi=fullName.replace('_hr.pdf', '.pdf'), infi=fullName)
subprocess.call(cmd, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

cmd = """
cd {dir}
gs -q -dNOPAUSE -dBATCH -dSAFER -dPDFA=2 -dPDFACompatibilityPolicy=1 -dSimulateOverprint=true -sDEVICE=pdfwrite -dCompatibilityLevel=1.3 -dPDFSETTINGS=/screen -dEmbedAllFonts=true -dSubsetFonts=true -dAutoRotatePages=/None -dColorImageDownsampleType=/Bicubic -dColorImageResolution=300 -dGrayImageDownsampleType=/Bicubic -dGrayImageResolution=300 -dMonoImageDownsampleType=/Bicubic -dMonoImageResolution=300 -sOutputFile={outfi} {infi}
""".format(dir=newdir, outfi=coverName.replace('_hr.pdf', '.pdf'), infi=coverName)
subprocess.call(cmd, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

print('\nGalleys for issue v{}n{} are in {}\n'.format(volume, number, issuedir) )

#eof
