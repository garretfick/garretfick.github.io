---
layout: post
title: Improved Design Pattern for Unit-Testable Event-Based (SAX) Parsers
date: 2012-06-18
---

Previously, I wrote about a design pattern for unit-testable event-based (SAX) parsers. At that time, I had used the pattern for a couple of parsers, and found it to be very successful. Since that time, I've used it for another parser that imposed some different restrictions. Rather than throw out the existing architecture, I found the design pattern was well suited to the different restrictions. The end result was an even better pattern, with fewer code paths.

First, what was the problem with the initial design? If you recall, the pattern consists of a stack of parsers. One of the arguments to the child parser is an object to accept the generated data. This works well only in limited situations where there is only one object that accepts the generated data. Where there are multiple, especially where they have different interfaces, the pattern requires switching depending on the supplied object.

An alternative and better approach is to use a delegate function/object to handle the generated data. In this way, the logic to handle the generated data can vary depending on the object.

Additionally, with this approach, we can omit the separate begin/finish functions, handling everything in `startElement` and `endElement`.

```
void CCustomerInfoMiniParser::CCustomerInfoMiniParser(std::function<void(Order*)> set_contact_delegate)
   : _set_contact_delegate(set_order_delegate)
{
}
void CCustomerInfoMiniParser::~CCustomerInfoMiniParser()
{
   //This will be not null in the case of an error
   delete _contact;
}
void CustomerInfoMiniParser::startElement(string& elementName, attributeMap& attrs)
{
   ++_depth;
   if (_depth == 1)
   {
      //We have started parsing customer information so create the member
      //that will contain the data
      _contact = new Contact;
   }
   else if (_depth == 2)
   {
      if (elementName.compare("Contact") == 0)
      {
         _contact->firstName = attrs.getAttribute("firstName");
         _contact->lastName = attrs.getAttribute("lastName");
      }
      ... // Handle other elements
      else
      {
         //If we didn't know what this element is, create a
         //null mini-parser to eat the elements (see the next section)
         _miniParser = new NullMiniParser();
         _miniParser-&amp;gt;startHandler(elementName, attrs);
         //This is the depth where we need to end the mini-parser
         //(see endElement)
         _miniParserEndDepth = 2;
      }
   }
}
void CustomerInfoMiniParser::endElement(string& elementName)
{
   
   //See the next section for details on the null mini-parser
   if (_miniParser != nullptr)
   {
      if (_depth == _miniParserEndDepth)
      {
         _miniParser->endHandler();
         delete _miniParser;
         _miniParser = nullptr;
      }
      else
      {
         _miniParser->endElement(elementName);
      }
   }
   if (_depth == 1)
   {
      _set_contact_delegate(_contact);
      _contact = nullptr;
   }
   --_depth;
}
```

Then when you create the `CustomerInfoMiniParser`, supply the delegate using an lambda. For example,

```
void OrderParser::startElement(string& elementName, attributeMap&; attrs)
{
   ++_depth;
   if (_depth == 2) //In this case, skip the root element, so start at 2
   {
      if (elementName.compare("CustomerInfo") == 0)
      {
         Order* order(order_);
         _miniParser = new CustomerInfoMiniParser([order](Contact* contact){order->setContact(contact);});
         //This and the following line create and initialize the mini parser that
         //will handle sub-elements, including the PaymentInfo. Notice that the
         //mini-parser gets the _order object, which is where it will add it's
         //parsed data
         _miniParser->startHandler(elementName, attrs);
      }
      ... //Add appropriate for each type at level of 2
   }
   else if (_depth > 2)
   {
      //Forward the event to the mini-parser
      _miniParser->startElement(elementName, attrs);
   }
}
```

Although things seem complex, with an appropriate abstract implementation of the `IMiniParser` interface, things get incredibly simple. I'm working on publishing the fully implemented example. Just be patient.
