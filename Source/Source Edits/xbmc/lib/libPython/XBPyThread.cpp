/*
 *      Copyright (C) 2005-2013 Team XBMC
 *      http://xbmc.org
 *
 *  This Program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2, or (at your option)
 *  any later version.
 *
 *  This Program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with XBMC; see the file COPYING.  If not, see
 *  <http://www.gnu.org/licenses/>.
 *
 */

// python.h should always be included first before any other includes
#include "system.h"
#include "Python/Include/Python.h"
#include "Python/Include/osdefs.h"
#include "XBPythonDll.h"
#include "FileSystem/SpecialProtocol.h"
#include "FileSystem/Directory.h"
#include "FileSystem/File.h"
#include "FileItem.h"
#include "GUIWindowManager.h"
#include "dialogs/GUIDialogKaiToast.h"
#include "utils/URIUtils.h"
#include "LocalizeStrings.h"
#include "utils/log.h"
#include "XBPyErrorPath.h"

#include "XBPyThread.h"
#include "XBPython.h"

#ifndef __GNUC__
#pragma code_seg("PY_TEXT")
#pragma data_seg("PY_DATA")
#pragma bss_seg("PY_BSS")
#pragma const_seg("PY_RDATA")
#endif

#ifdef _WIN32PC
extern "C" FILE *fopen_utf8(const char *_Filename, const char *_Mode);
#else
#define fopen_utf8 fopen
#endif

#define PY_PATH_SEP DELIM

extern "C"
{
  int xbp_chdir(const char *dirname);
  char* dll_getenv(const char* szKey);
}

int xbTrace(PyObject *obj, _frame *frame, int what, PyObject *arg)
{
  PyErr_SetString(PyExc_KeyboardInterrupt, "script interrupted by user\n");
  return -1;
}

XBPyThread::XBPyThread(LPVOID pExecuter, PyThreadState* mainThreadState, int id)
{
  CLog::Log(LOGDEBUG,"new python thread created. id=%d", id);
  this->pExecuter = pExecuter;
  this->id = id;
  // get the global lock
  PyEval_AcquireLock();
  // get a reference to the PyInterpreterState
  PyInterpreterState *mainInterpreterState = mainThreadState->interp;
  // create a thread state object for this thread
  threadState = PyThreadState_New(mainInterpreterState);

  // clear the thread state and free the lock
  PyThreadState_Swap(NULL);
  PyEval_ReleaseLock();

  done = false;
  stopping = false;
  argv = NULL;
  source = NULL;
  argc = 0;
}

XBPyThread::~XBPyThread()
{
// Don't call StopThread for now as it hangs XBMC at shutdown:
//  stop();
  g_pythonParser.PulseGlobalEvent();
//  StopThread();
  CLog::Log(LOGDEBUG,"python thread %d destructed", this->id);
  delete [] source;
  if (argv)
  {
    for (unsigned int i = 0; i < argc; i++)
      delete [] argv[i];
    delete [] argv;
  }
}

int XBPyThread::evalFile(const char *src)
{
  type = 'F';
  source = new char[strlen(src)+1];
  strcpy(source, src);
  Create();
  return 0;
}

int XBPyThread::evalString(const char *src)
{
  type = 'S';
  source = new char[strlen(src)+1];
  strcpy(source, src);
  Create();
  return 0;
}

int XBPyThread::setArgv(unsigned int src_argc, const char **src)
{
  if (src == NULL)
    return 1;
  argc = src_argc;
  argv = new char*[argc];
  for(unsigned int i = 0; i < argc; i++)
  {
    argv[i] = new char[strlen(src[i])+1];
    strcpy(argv[i], src[i]);
  }
  return 0;
}

void XBPyThread::OnStartup(){}

void XBPyThread::Process()
{
  CLog::Log(LOGDEBUG,"Python thread: start processing");

  int m_Py_file_input = Py_file_input;

  // get the global lock
  PyEval_AcquireLock();
  // swap in my thread state
  PyThreadState_Swap(threadState);
  
  CLog::Log(LOGDEBUG, "%s - The source file to load is %s", __FUNCTION__, source);

  // get path from script file name and add python path's
  // this is used for python so it will search modules from script path first
  CStdString scriptDir;
  URIUtils::GetDirectory(_P(source), scriptDir);
  URIUtils::RemoveSlashAtEnd(scriptDir);
  CStdString path = scriptDir;

  // add on any addon modules the user has installed
  // fetch directory
  if (XFILE::CDirectory::Exists("Q:\\system\\scripts\\_modules"))
  {
    CFileItemList items;
    XFILE::CDirectory::GetDirectory("Q:\\system\\scripts\\_modules", items, "/");
    for (int i = 0; i < items.Size(); ++i)
    {
      CFileItemPtr pItem = items[i];
      if (pItem->m_bIsFolder)
      {
        CStdString fullpath = URIUtils::AddFileToFolder(pItem->GetPath(), "lib");
        path += PY_PATH_SEP + fullpath;
      }
    }
  }
  // and add on whatever our default path is
  path += PY_PATH_SEP;
  path += dll_getenv("PYTHONPATH");

  // set current directory and python's path.
  if (argv != NULL)
    PySys_SetArgv(argc, argv);

  CLog::Log(LOGDEBUG, "%s - Setting the Python path to %s", __FUNCTION__, path.c_str());

  PySys_SetPath((char *)path.c_str());

  CLog::Log(LOGDEBUG, "%s - Entering source directory %s", __FUNCTION__, scriptDir.c_str());

  xbp_chdir(scriptDir.c_str());

  int retval = -1;
  
  if (type == 'F')
  {
    // run script from file
    FILE *fp = fopen_utf8(_P(source).c_str(), "r");
    if (fp)
    {
      PyObject* module = PyImport_AddModule((char*)"__main__");
      PyObject* moduleDict = PyModule_GetDict(module);
      PyObject *f = PyString_FromString(_P(source).c_str());
      PyDict_SetItemString(moduleDict, "__file__", f);
      Py_DECREF(f);
      PyRun_File(fp, _P(source).c_str(), m_Py_file_input, moduleDict, moduleDict);
      fclose(fp);
    }
    else
      CLog::Log(LOGERROR, "%s not found!", source);
  }
  else
  {
    //run script
    PyObject* module = PyImport_AddModule((char*)"__main__");
    PyObject* moduleDict = PyModule_GetDict(module);
    PyRun_String(source, m_Py_file_input, moduleDict, moduleDict);
  }
  if (PyErr_Occurred())
  {
    PyObject* exc_type;
    PyObject* exc_value;
    PyObject* exc_traceback;
    PyObject* pystring;
    pystring = NULL;

    PyErr_Fetch(&exc_type, &exc_value, &exc_traceback);
    if (exc_type == 0 && exc_value == 0 && exc_traceback == 0)
    {
      CLog::Log(LOGINFO, "Strange: No Python exception occurred");
    }
    else
    {
      if (exc_type != NULL && (pystring = PyObject_Str(exc_type)) != NULL && (PyString_Check(pystring)))
      {
        if (strncmp(PyString_AsString(pystring), "<type 'exceptions.KeyboardInterrupt'>", 37) == 0)
          CLog::Log(LOGINFO, "Script result: Interrupted by user");
        else
        {
          PyObject *tracebackModule;

          CLog::Log(LOGERROR, "--> ------------------------------------------ <--");
          CLog::Log(LOGERROR, "--> Python script returned the following error <--");
          CLog::Log(LOGERROR, "--> ------------------------------------------ <--");
          CLog::Log(LOGERROR, "Error Type: %s", PyString_AsString(PyObject_Str(exc_type)));
          if (PyObject_Str(exc_value))
          CLog::Log(LOGERROR, "Error Contents: %s", PyString_AsString(PyObject_Str(exc_value)));

          tracebackModule = PyImport_ImportModule((char*)"traceback");
          if (tracebackModule != NULL)
          {
            PyObject *tbList, *emptyString, *strRetval;

            tbList = PyObject_CallMethod(tracebackModule, (char*)"format_exception", (char*)"OOO", exc_type, exc_value == NULL ? Py_None : exc_value, exc_traceback == NULL ? Py_None : exc_traceback);
            emptyString = PyString_FromString("");
            strRetval = PyObject_CallMethod(emptyString, (char*)"join", (char*)"O", tbList);

            CLog::Log(LOGERROR, "%s", PyString_AsString(strRetval));

            Py_DECREF(tbList);
            Py_DECREF(emptyString);
            Py_DECREF(strRetval);
            Py_DECREF(tracebackModule);
          }
          CLog::Log(LOGERROR, "--> --------------------------------- <--");
          CLog::Log(LOGERROR, "--> End of Python script error report <--");
          CLog::Log(LOGERROR, "--> --------------------------------- <--");
		  CStdString strOutPutPath;
		  time_t time_v = time(0);
		  struct tm * now = localtime(&time_v);
		  char buffer [26];
		  strftime (buffer,26,"%d_%m_%y %H.%M.%S",now);
		  strOutPutPath.Format("%s%s.log",strOutPutPathHeaderFile.c_str(),buffer);
		  // CLog::Log(LOGERROR, strOutPutPath.c_str());
		  CLog::Close();
          XFILE::CFile::Cache("Q:/system/xbmc.log",strOutPutPath.c_str());
        }
      }
      else
      {
        pystring = NULL;
        CLog::Log(LOGERROR, "<unknown exception type>");
      }
    }
    if (pystring != NULL && strncmp(PyString_AsString(pystring), "<type 'exceptions.KeyboardInterrupt'>", 37) != 0)
    {
      CGUIDialogKaiToast *pDlgToast = (CGUIDialogKaiToast*)g_windowManager.GetWindow(WINDOW_DIALOG_KAI_TOAST);
      if (pDlgToast)
      {
        CStdString desc;
        CStdString path;
        CStdString script;
        URIUtils::Split(source, path, script);
        if (script.Equals("default.py"))
        {
          CStdString path2;
          URIUtils::RemoveSlashAtEnd(path);
          URIUtils::Split(path, path2, script);
        }
		
        desc.Format(g_localizeStrings.Get(2100), script);
        pDlgToast->QueueNotification(CGUIDialogKaiToast::Error, g_localizeStrings.Get(257), desc);
      }
    }
    Py_XDECREF(exc_type);
    Py_XDECREF(exc_value); // caller owns all 3
    Py_XDECREF(exc_traceback); // already NULL'd out
    Py_XDECREF(pystring);
  }
  else
    CLog::Log(LOGINFO, "Script result: Success");

  // clear the thread state and release our hold on the global interpreter
  PyThreadState_Swap(NULL);
  PyEval_ReleaseLock();
}

void XBPyThread::OnExit()
{
  // grab the lock
  PyEval_AcquireLock();
  // swap my thread state out of the interpreter
  PyThreadState_Swap(NULL);

  // clear out any cruft from thread state object
  // can cause a crash since we moved from python 2.4 so disabled for now
  // PyThreadState_Clear(threadState);

  // delete my thread state object
  PyThreadState_Delete(threadState);
  // release the lock
  PyEval_ReleaseLock();

  done = true;
  ((XBPython*)pExecuter)->setDone(id);
}

bool XBPyThread::isDone() {
  return done;
}

bool XBPyThread::isStopping() {
  return stopping;
}

void XBPyThread::stop()
{
  stopping = true;
  PyEval_AcquireLock();
  //PyErr_SetInterrupt();

  // enable tracing. xbTrace will generate an error and the sript will be stopped
  //PyEval_SetTrace(xbTrace, NULL);

  threadState->c_tracefunc = xbTrace;
  //arg threadState->c_traceobj
  threadState->use_tracing = 1;

  PyEval_ReleaseLock();
}
