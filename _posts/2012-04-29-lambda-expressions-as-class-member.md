---
layout: post
title: Lambda Expressions as Class Member
date: 2012-04-29
---

Recently I've been refactoring code to make it unit testable. Due to the way the code words, I needed to create a stub that included some unit test assertions. In fact, I needed a lot of very similar stubs, the difference being only in the assertions. One way to do this is to use a common stub, and outfit it with a different functor for each test.

I thought it must be possible to use the C++ lambda's to write even less code. The answer is yes, and the code below shows how to achieve this.

```
#include <functional>
#include <iostream>
#include <string>
using namespace std;
class Animal
{
public:
   void SetSound(function<string(void)> p_sound) { sound = p_sound; }
   void MakeSound() { cout << sound() << endl; }
private:
   function<string(void)> sound;
};
int main()
{
   Animal dog;
   dog.SetSound([]() { return string("Woof"); });
   dog.MakeSound();
   return 0;
}
```