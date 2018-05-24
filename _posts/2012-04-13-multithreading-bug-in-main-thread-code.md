---
layout: post
title: Multithreading Bug in Main Thread Code
date: 2012-04-13
---

Is is possible for code that is only executed in the main thread to behave as through multi-threads were accessing the code? To help answer the question, assume you are a Windows MFC application. That is probably still not clear enough, so lets see some code.

```
class CMyClass
{
   public:
   CMyClass() { hDone = ::CreateEvent(NULL, TRUE, FALSE, NULL); }
   ~CMyClass() { ::CloseHandle(hDone); }
   void MainThreadFunction()
   {
      ::ResetEvent(hDone);
      ::CreateThread(NULL, 0, ThreadFunc, reinterpret_cast<LPVOID>(hDone), 0, NULL);
      WaitFunction(hDone);
   }
   void WaitFunction(HANDLE hDone)
   {
      //Wait on the handle
   }
};

DWORD ThreadFunc(LPVOID lpThreadParam)
{
   HANDLE hDone = reinterpret_cast&lt;HANDLE&gt;(lpThreadParam);
   Sleep(1000); //Simulate some work
   ::SetEvent(hDone);
}
```

The class has a single event that is resued each time `MainThreadFunction` is called. `MainThreadFunction`creates a thread to run `ThreadFunc`, a thread-safe function, and waits for the thread to complete before returning. Resuing the event in this way is safe, provided that you don't recursively call `CMyClass::MainThreadFunction`. If `CMyClass::MainThreadFunction` is called recursively, the code may hang (I'll leave it as an excersise to show why, and why the answer is also not definitive). Whether the code recursively calls `CMyClass::MainThreadFunction` entirely depends on what happens in `WaitFunction` (and is the source of the bug I uncovered today).

Often, `CMyClass::WaitFunction` looks something like

```
void WaitFunction(HANDLE hDone)
{
   WaitForSingleObject(hDone, INFINITE);
}
```

But suppose you want to process messages while waiting so that your application doesn't appear to hang, for example, by using `MsgWaitForMultipleObjects`. Now the potential for disaster should be obvious. If one of those messages calls `CMyClass::MainThreadFunction`, you have recursively called the function, and whether you hang is just luck of the draw. The lesson of the day is, think very carefully before processing messages while waiting.