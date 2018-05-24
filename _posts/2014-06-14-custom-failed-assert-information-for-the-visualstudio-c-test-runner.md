---
layout: post
title: Custom Failed Assert Information for the VisualStudio C# Test Runner
date: 2014-06-14
---

I was recently debugging an intermitent test failure that would only occur on a machine I couldn't access, so I wanted to output some additional information about the test failure.

My solution was to append information to the test output when an assert fails. The following is the basic framework I used to capture and add information to the test result.

```
using System;
using System.Runtime.Serialization;
using Microsoft.VisualStudio.TestTools.UnitTesting;
namespace CustomAssertException
{
    [TestClass]
    public class UnitTest
    {
        [TestMethod]
        public void TestMethod1()
        {
            try
            {
                Assert.AreEqual(2, 4);
            }
            catch (AssertFailedException ex)
            {
                throw new CustomAssertFailedException(ex, new CustomAssertInfo());
            }
        }
    }
 
    /// The custom information. This class should do no work unless the ToString /// method is called.
    public class CustomAssertInfo
    {
        public override string ToString()
        {
            return "Custom assert text";
        }
    }
 
    /// Exception class that the test runner will catch and print out the message.
    [Serializable]
    public class CustomAssertFailedException : AssertFailedException
    {
        private CustomAssertInfo _customInfo;
        public CustomAssertFailedException(AssertFailedException ex, CustomAssertInfo customInfo) : base(String.Empty, ex)
        {
            _customInfo = customInfo;
        }
        public CustomAssertFailedException(SerializationInfo info, StreamingContext context)
        {
             
        }
        public override string Message
        {
            get
            {
                return InnerException.Message + _customInfo;
            }
        }
    }
}
```