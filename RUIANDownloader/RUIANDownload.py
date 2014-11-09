# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        RUIANDownload
# Purpose:
#
# Author:      Radek Augustýn
#
# Copyright:   (c) Radek Augustýn 2014
#-------------------------------------------------------------------------------
from cgitb import html

DEBUG_MODE = False

__author__ = 'raugustyn'

# ####################################
# Standard modules import
# ####################################
import urllib2
import gzip
import os
import sys
import datetime

import shared; shared.setupPaths()

# ####################################
# Specific modules import
# ####################################
from log import logger, clearLogFile
from infofile import infoFile
from htmllog import htmlLog

from SharedTools.config import pathWithLastSlash
from SharedTools.config import Config
from SharedTools.sharetools import safeMkDir

def convertRUIANDownloadCfg(config):
    if config == None: return

    def isTrue(value):
        return value != None and value.lower() == "true"

    config.downloadFullDatabase = isTrue(config.downloadFullDatabase)
    config.uncompressDownloadedFiles = isTrue(config.uncompressDownloadedFiles)
    config.runImporter = isTrue(config.runImporter)
    config.dataDir = pathWithLastSlash(config.dataDir)
    config.ignoreHistoricalData = isTrue(config.ignoreHistoricalData)
    infoFile.load(config.dataDir + "info.txt")
    pass

config = Config("RUIANDownload.cfg",
            {
                "downloadFullDatabase" : False,
                "uncompressDownloadedFiles" : False,
                "runImporter" : False,
                "dataDir" : "DownloadedData\\",
                "downloadURLs" : "http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=" + \
                                 "U&vf.up=ST&vf.ds=K&vf.vu=Z&_vf.vu=on&_vf.vu=on&vf.vu=H&_vf.vu=on&_vf.vu=on&search=Vyhledat;" + \
                                 "http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=U&" +\
                                 "vf.up=OB&vf.ds=K&vf.vu=Z&_vf.vu=on&_vf.vu=on&_vf.vu=on&_vf.vu=on&vf.uo=A&search=Vyhledat",
                "ignoreHistoricalData": True
            },
           convertRUIANDownloadCfg,
           defSubDir = "RUIANDownloader",
           moduleFile = __file__)

def extractFileName(fileName):
    lastDel = fileName.rfind(os.sep)
    return fileName[lastDel + 1:]


def getFileExtension(fileName):
    """ Returns fileName extension part dot including (.txt,.png etc.)"""
    return fileName[fileName.rfind("."):]


def ___filePercentageInfo(fileSize, downloadedSize):
    status = r"%10d  [%3.2f%%]" % (downloadedSize, downloadedSize * 100. / fileSize)
    logger.info(status)

filePercentageInfo = ___filePercentageInfo


def __fileDownloadInfo(fileName, fileSize):
    #logger.info("   Size %s Bytes" % (fileSize))
    # intentionally blank
    pass

fileDownloadInfo = __fileDownloadInfo


class DownloadInfo:
    def __init__(self):
        self.fileName = ""
        self.fileSize = 0
        self.compressedFileSize = 0
        self.downloadTime = 0
        pass


def cleanDirectory(folder):
    if os.path.exists(folder):
        for the_file in os.listdir(folder):
            path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    cleanDirectory(path)
                    os.rmdir(path)

            except Exception, e:
                logger.error(e.message, str(e))


def getFileContent(fileName):
    logger.debug("getFileContent")
    with open(fileName, "r") as f:
        lines = f.read().splitlines()
        f.close()
    return lines


def formatTimeDelta(timeDelta):
    v = str(timeDelta)

    #s = timeDelta.seconds
    #hours = s // 3600
    # remaining seconds
    #s = s - (hours * 3600)
    # minutes
    #minutes = s // 60
    # remaining seconds
    #seconds = s - (minutes * 60)

    v = v.strip("0")
    if v[0:1] == ".": v = "0" + v
    if v == "": v = "0"
    return v + "s"

def getUpdateURL(url, dateStr):
    url = url.replace("vf.cr=U&", "vf.cr=Z&")
    url = url.replace("vf.up=ST&", "")
    url = url.replace("vf.up=OB&", "")
    url = url.replace("vf.vu=Z&", "")
    url = url.replace("vf.uo=A&", "")
    url += "&vf.pd=" + dateStr
    return url

class RUIANDownloader:
    def __init__(self, aTargetDir = ""):
        self._targetDir = ""
        self.setTargetDir(aTargetDir)
        self.downloadInfos = []
        self.downloadInfo = None
        self._fullDownload = True
        self.pageURLs = config.downloadURLs
        self.ignoreHistoricalData = config.ignoreHistoricalData
        pass

    def getTargetDir(self):
        return self._targetDir

    def setTargetDir(self, aTargetDir):
        if aTargetDir != "":
            if aTargetDir.rfind("\\") != len(aTargetDir) - 1:
                aTargetDir += "\\"
            if not os.path.exists(aTargetDir):
                os.makedirs(aTargetDir)
        self._targetDir = aTargetDir
        pass

    targetDir = property(fget = getTargetDir, fset = setTargetDir)

    def getFullSetList(self):
        logger.debug("RUIANDownloader.getFullSetList")
        self._fullDownload = True
        return self.getList(self.pageURLs)

    def getList(self, urls):
        urls = urls.split(";")
        result = []
        for url in urls:
            url = url.replace("vyhledej", "seznamlinku")
            logger.info("Downloading file list from " + url)
            content = urllib2.urlopen(url).read()
            lines = content.splitlines()
            result.extend(lines)
            #break

        if self.ignoreHistoricalData:
            newResult = []
            stateMonth = datetime.date.today().month - 1
            for url in result:
                date = url[url.rfind("/") + 1:]
                date = date[:date.find("_")]
                month = int(date[4:6])
                if month >= stateMonth:
                    newResult.append(url)
            result = newResult

        if DEBUG_MODE:
            result = result[:5]
            #result = result[len(result)-5:]
        return result

    def getUpdateList(self, fromDate = ""):
        logger.debug("RUIANDownloader.getUpdateList since %s", infoFile.validFor())
        self._fullDownload = False
        if fromDate == "" or infoFile.validFor() != "":
            v = infoFile.validFor()
            dateStr = v[8:10] + "." + v[5:7] + "." + v[0:4]
            firstPageURL = self.pageURLs.split(";")[0]
            return self.getList(getUpdateURL(firstPageURL, dateStr))
        else:
            return []

    def buildIndexHTML(self):
        def addCol(value, tags = ""):
            htmlLog.addCol(value, tags)

        def addDownloadHeader():
            if self._fullDownload:
                headerText = "Stažení stavových dat"
            else:
                headerText = "Stažení aktualizací k "
            v = str(datetime.datetime.now())
            htmlLog.addHeader(headerText + " " + v[8:10] + "." + v[5:7] + "." + v[0:4])

        def addTableHeader():
            htmlLog.openTable()
            htmlLog.htmlCode += "<tr><th align='left' valign='bottom'>Soubor</th><th>Staženo<br>[Bajtů]</th>"
            if config.uncompressDownloadedFiles:
                htmlLog.htmlCode += "<th></th><th>Rozbaleno<br>[Bajtů]</th>"
            htmlLog.htmlCode += "<th valign='bottom'>Čas</th></tr>"

        def calcSumValues():
            calcInfo = DownloadInfo()
            calcInfo.downloadTime = 0
            for info in self.downloadInfos:
                if info.downloadTime == "":
                    return
                elif info.fileName != "":
                        calcInfo.fileSize += info.fileSize
                        calcInfo.compressedFileSize += info.compressedFileSize
                        logger.info(info.fileName + ":" + info.downloadTime)
                        time = float(info.downloadTime[:len(info.downloadTime) - 1])
                        calcInfo.downloadTime = calcInfo.downloadTime + time
                else:
                    info.fileSize = calcInfo.fileSize
                    info.compressedFileSize = calcInfo.compressedFileSize
                    info.downloadTime = calcInfo.downloadTime
                    return

            calcInfo.downloadTime = str(calcInfo.downloadTime) + "s"
            self.downloadInfos.append(calcInfo)

        def intToStr(intValue):
            if int == 0:
                return ""
            else:
                return str(intValue)

        def addTableContent():
            altColor = True
            for info in self.downloadInfos:
                if altColor:
                    tags = 'class="altColor"'
                else:
                    tags = ''
                altColor = not altColor
                htmlLog.openTableRow(tags)

                addCol(extractFileName(info.fileName))

                addCol(intToStr(info.compressedFileSize), 'align="right"')

                if config.uncompressDownloadedFiles and info.fileSize != 0:
                    addCol("->")
                else:
                    addCol("")

                if config.uncompressDownloadedFiles:
                    addCol(intToStr(info.fileSize), "align=right")

                addCol(info.downloadTime, "align=right")
                htmlLog.closeTableRow()
            htmlLog.closeTable()

        htmlLog.clear()
        addDownloadHeader()
        addTableHeader()
        calcSumValues()
        addTableContent()
        htmlLog.save(config.dataDir + "index.html")
        pass

    def downloadURLList(self, urlList):

        def buildDownloadInfosList():
            self.downloadInfos = []
            for href in urlList:
                self.downloadInfo = DownloadInfo()
                self.downloadInfo.fileName = href.split('/')[-1]
                self.downloadInfos.append(self.downloadInfo)

        logger.debug("RUIANDownloader.downloadURLList")
        buildDownloadInfosList()
        index = 0
        for href in urlList:
            self.downloadInfo = self.downloadInfos[index]
            index = index + 1
            fileName = self.downloadURLtoFile(href, index, len(urlList))
            if config.uncompressDownloadedFiles:
                self.uncompressFile(fileName, True)
        self.buildIndexHTML()
        pass

    def downloadURLtoFile(self, url, fileIndex, filesCount):
        # Downloads to temporary file, if suceeded, then rename result
        tmpFileName = pathWithLastSlash(self.targetDir) + "tmpfile.bin"
        logger.debug("RUIANDownloader.downloadURLtoFile")
        file_name = self.targetDir + url.split('/')[-1]
        startTime = datetime.datetime.now()

        if os.path.exists(file_name):
            logger.info("File " + extractFileName(file_name) + " is already downloaded, skipping it.")
            fileSize = os.stat(file_name).st_size
        else:
            req = urllib2.urlopen(url)
            meta = req.info()
            fileSize = int(meta.getheaders("Content-Length")[0])
            logger.info("Downloading file %s [%d/%d %d Bytes]" % (extractFileName(file_name), fileIndex, filesCount, fileSize))
            fileDownloadInfo(file_name, fileSize)
            CHUNK = 1024*1024
            file_size_dl = 0
            with open(tmpFileName, 'wb') as fp:
                while True:
                    chunk = req.read(CHUNK)
                    if not chunk:
                        break
                    fp.write(chunk)
                    file_size_dl += len(chunk)
                    logger.info(r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100.0 / fileSize))
                    self.downloadInfo.compressedFileSize = file_size_dl
                    #self.buildIndexHTML()
            fp.close()
            os.rename(tmpFileName, file_name)

        self.downloadInfo.downloadTime = formatTimeDelta(str(datetime.datetime.now() - startTime)[5:])
        self.downloadInfo.fileName = file_name
        self.downloadInfo.compressedFileSize = fileSize
        return file_name

    def uncompressFile(self, fileName, deleteSource = True):
        """
        Tato metoda rozbalí soubor s názvem fileName.

        @param fileName: Název souboru k dekompresi
        @param deleteSource: Jestliže True, komprimovaný soubor bude vymazán.
        @return: Vrací název expandovaného souboru.
        """
        logger.debug("RUIANDownloader.uncompressFile")
        ext = getFileExtension(fileName).lower()
        if ext == ".gz":
            outFileName = fileName[:-len(ext)]
            logger.info("Uncompressing " + extractFileName(fileName) + " -> " + extractFileName(outFileName))
            f = gzip.open(fileName, 'rb')
            # @TODO tady by se melo cist po kouskach
            fileContent = f.read()
            f.close()
            out = open(outFileName, "wb")
            out.write(fileContent)
            self.downloadInfo.fileSize = len(fileContent)
            out.close()
            if deleteSource:
                os.remove(fileName)
            return outFileName
        else:
            return fileName

    def download(self):
        def wasItToday(dateTimeStr):
            if dateTimeStr == "":
                return False
            else:
                return str(datetime.datetime.now().date()) == dateTimeStr.split(" ")[0]

        if not infoFile.fullDownloadBroken:
            if wasItToday(infoFile.lastFullDownload):
                logger.warning("Process stopped! Nothing to download. Last full download was done Today " + infoFile.lastFullDownload)
                return
            elif not self._fullDownload and wasItToday(infoFile.lastPatchDownload):
                logger.warning("Process stopped! Nothing to download. Last patch was downloaded Today " + infoFile.lastPatchDownload)
                return

        startTime = datetime.datetime.now()

        callUpdate = False;
        if self._fullDownload or infoFile.lastFullDownload == "":
            logger.info("Running in full mode")
            if not infoFile.fullDownloadBroken:
                logger.info("Cleaning directory " + config.dataDir)
                cleanDirectory(config.dataDir)
                infoFile.fullDownloadBroken = True
                infoFile.save()

            safeMkDir(config.dataDir)

            l = self.getFullSetList()
            d = datetime.date.today()
            infoFile.lastFullDownload = '{:04d}'.format(d.year) + "-" + '{:02d}'.format(d.month) + "-01 14:07:13.084000"
            infoFile.lastPatchDownload = ""
            callUpdate = True

        else:
            logger.info("Running in update mode")
            l = self.getUpdateList()
            infoFile.lastPatchDownload = str(datetime.datetime.now())

        self.buildIndexHTML()

        if len(l) > 0:   # stahujeme jedině když není seznam prázdný
            self.downloadURLList(l)
            infoFile.save()
            self.saveFileList(l)
        else:
            logger.warning("Nothing to download, list is empty.")

        self.buildIndexHTML()
        htmlLog.closeSection(config.dataDir + "index.html")

        infoFile.fullDownloadBroken = False
        infoFile.save()

        if callUpdate:
            self._fullDownload = False
            self.download()

    def saveFileList(self, fileList):
        infoFile.numPatches = infoFile.numPatches + 1
        v = str(datetime.datetime.now())
        fileName = v[0:4] + "." + v[5:7] + "." + v[8:10] + ".txt"
        if self._fullDownload:
            fileName = "Download_" + fileName
        else:
            fileName = "Patch_" + fileName
        outFile = open(config.dataDir + fileName, "w")
        for line in fileList:
            outFile.write(line + "\n")
        outFile.close()

    def _downloadURLtoFile(self, url):
        logger.debug("RUIANDownloader._downloadURLtoFile")
        logger.info("Downloading " + url)
        file_name = url.split('/')[-1]
        logger.info(file_name)
        u = urllib2.urlopen(url)
        f = open(self.targetDir + file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        logger.info("Downloading %s Bytes: %s" % (file_name, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            blockBuffer = u.read(block_sz)
            if not blockBuffer:
                break

            file_size_dl += len(blockBuffer)
            f.write(blockBuffer)
            filePercentageInfo(file_size, file_size_dl)
        f.close()
        pass


def printUsageInfo():
    logger.info(u'Použití: RUIANDownload.py [-DownloadFullDatabase {True | False}] [-DataDir data_dir] [-UncompressDownloadedFiles {True | False}][-help]')
    logger.info('')
    sys.exit(1)

def getDataDirFullPath():
    result = config.dataDir
    if not os.path.isabs(config.dataDir):
        result = os.path.dirname(config.moduleFile) + os.path.sep + config.dataDir
        result = os.path.normpath(result)
        result = pathWithLastSlash(result)
    return result

def main(argv = sys.argv):
    if (argv is not None) or (len(argv) > 1):
        i = 1
        while i < len(argv):
            arg = argv[i].lower()

            if arg == "-downloadfulldatabase":
                i = i + 1
                config.downloadFullDatabase = argv[i].lower() == "True"
            elif arg == "-datadir":
                i = i + 1
                config.dataDir = pathWithLastSlash(argv[i])
                if not os.path.exists(config.dataDir):
                    logger.error("DataDir %s does not exist", config.dataDir)
                    printUsageInfo()
            elif arg == "-uncompressdownloadedfiles":
                i = i + 1
                config.uncompressDownloadedFiles = argv[i].lower() == "True"
            else:
                logger.error('Unrecognised command option: %s' % arg)
                printUsageInfo()

            i = i + 1
            # while exit

        if config.downloadFullDatabase:
            clearLogFile()

        logger.info("RUIANDownloader")
        logger.info("#############################################")
        logger.info("Data directory : %s", config.dataDir)
        logger.info("Data directory full path : %s", getDataDirFullPath())
        logger.info("Download full database : %s", str(config.downloadFullDatabase))
        if not config.downloadFullDatabase:
            logger.info("Last full download  : %s", infoFile.lastFullDownload)
            logger.info("Last patch download : %s", infoFile.lastPatchDownload)
        logger.info("---------------------------------------------")

        downloader = RUIANDownloader(config.dataDir)
        downloader._fullDownload = config.downloadFullDatabase or infoFile.fullDownloadBroken
        downloader.download()

        logger.info("Download done.")
        if config.runImporter:
            from RUIANImporter.importRUIAN import doImport
            doImport()

if __name__ == '__main__':
    main()