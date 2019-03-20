---
id: XDN07
title: xmeta Semantic Checking
author: t-tiroma@microsoft.com
status: draft
---

# Title: XDN11 - xmeta Semantic Checking

- Author: Tim Romanski (t-tiroma@microsoft.com)
- Status: draft

## Abstract

This design note specifies the semantic checks performed when generating metadata files from xlang IDL files. The checks are based on the Class Declaration Language (CDL) specification and the xlang Type System. The categories to be checked are namespaces, types, and members of namespaces and of each type.

Types include classes, structs, interfaces, enums, and delegates.

### Namespaces

### Namespace members

##### Definitions:
A **declaration space** is defined by namespace declarations. Each namespace has its own unique declaration space, and outside of all namespaces is a special declaration space called the **global declaration space**. The scope of the global declaration space is limited to the IDL file it is contained in.

The scope defined by an IDL file is called a **compilation unit**.

**Namespace members** include nested namespace declarations and type declarations.

**Types** include classes, structs, interfaces, enums, and delegates.

Namespaces can include other namespaces with a **using namespace directive**. This has syntax `using <namespace-name>`. This allows members from the included namespace to be referenced.

You can also include namespaces or types through a **using alias directive**. This has syntax `using <identifier> = <namespace-or-type-name>;`.

A **namespace alias qualifier** refers to a namespace or a type. It guarantees that type name lookups are unaffected by the introduction of new types and members. This has syntax `identifier::identifier<A1,...,Ak>` where `<A1,...,Ak>` is optional.  

##### Checks:
Only types from the declaration space of included namespaces can be referenced. This means that types from nested namespaces are unavailable, since they belong to a separate declaration space.
For example:
```
namespace N1
{
    class A { }
    namespace N2
    {
        class B { }
    }
}

namespace N3
{
    using N1;
    class C: A { } // OK
    class D: B { } // Error, B is in N1.N2's declaration space, which is not included.
}
```
Class B was referenced, but its declaration space was not included. This is an error.

If two namespaces included define members with the same name, and the including namespace references that member name, it is ambiguous and is an error.

Namespace members in the same declaration space cannot have the same name.

The identifier of a using alias directive must be unique within its declaration space, and cannot be the same as any member defined in the declaration space.
For example:
```
namespace N3
{
    class B { }
}
namespace N3
{
    using E = N1.A;    // OK
    using E = N1.N2.B; // Error, E already exists in N3.
    using B = N1.N2.B; // Error, B already exists in N3.
}
```

Any referenced using alias directive must be defined in the namespace body or compilation unit in which it occurs.
For example:
```
using R = N1.N2;
namespace N3
{
    using S = N1;
    class C: R.B { } // OK, since R is defined in the compilation unit.
}
namespace N3
{
    class D: S.A; // Error, since S is not defined in the current namespace body or compilation unit.
}
```

Using aliases can name a closed constructed type like `using Y = N1.A<Int32>;`, however the type argument cannot be generic.

For namespace alias qualifiers, they have the form `N::I<A1,...,Ak>`.
* If N is the identifier 'global', then the global namespace is searched for I. One of the following must be true:
  * The global namespace contains a namespace named I and K is zero.
  * The global namespace contains a non-generic type named I and K is zero.
  * The global namespace contains a type named I that has K type parameters.
* Otherwise, search the immediate containing namespace then each enclosing namespace until the a matching entity is located. N must be associated with a namespace with an extern alias directive or using alias directive, and one of the following must be true:
  * The namespace associated with N contains a namespace named I and K is zero.
  * The namespace associated with N contains a type named I with K type arguments.



### Classes

### Class members

### Structs

### Struct members

### Interfaces
1) It is a compile-time error for an interface to directly or indirectly inherit from itself.

2) All Xlang interfaces must inherit directly from IInspectable, which in turn inherits from IUnknown.

3) Interfaces Requires:
Interfaces may specify that they require one or more other interfaces that must be implemented on any object that implements the current interface. For example, if IButton required IControl then any class implementing IButton would also need to implement IControl.
Adding new functionality by implementing new interfaces that inherit from existing interfaces (i.e. IFoo2 inherits from IFoo) is not allowed. (How is this different from require interfaces???)
The required interfaces of an interface are the explicit required interfaces and their required interfaces. In other words, the set of required interfaces is the complete transitive closure of the explicit required interfaces, their explicit required interfaces, and so on. In the example
interface IControl
{
	void Paint();
}
interface ITextBox: IControl
{
	void SetText(String text);
}
interface IListBox: IControl
{
	void SetItems(String[] items);
}
interface IComboBox: ITextBox, IListBox {}
the required interfaces of IComboBox are IControl, ITextBox, and IListBox.

A class that implements an interface also implicitly implements all of the interface’s required interfaces. (What does implicitly means in this case?)

The members of an interface are the members declared by the interface itself, but do not include the members from the required interface

4) Parameterized Interface
A required interface of a parameterized interface may share the same type argument list, such that a single type argument is used to specify the parameterized instance of both the interface and the interface it requires (eq IVector<T> requires IIterable<T>). The signature of any member (aka method, property or event) of a parameterized interface may reference a type from the parameterized interface’s type arguments list. (eq. IVector<T>.SetAt([in] UInt32 index, [in] T value)).

The inherited members of an interface are specifically not part of the declaration space of the interface. Thus, an interface is allowed to declare a member with the same name or signature as an inherited member. 

5) The interfaces referenced by a generic type declaration must remain unique for all possible constructed types. Without this rule, it would be impossible to determine the correct method to call for certain constructed types. For example, suppose a generic class declaration were permitted to be written as follows:
interface I<T>
{
	   void F();
}
class X<U,V>: I<U>, I<V>					// Error: I<U> and I<V> conflict

To determine if the interface list of a generic type declaration is valid, the following steps are performed:
•	Let L be the list of interfaces directly specified in a generic class, struct, or interface declaration C.
•	Add to L any required interface of the interfaces already in L.
•	Remove any duplicates from L.
•	If any possible constructed type created from C would, after type arguments are substituted into L, cause two interfaces in L to be identical, then the declaration of C is invalid

### Interface members
1) The name of a method must differ from the names of all properties and events declared in the same interface. 

The signature of a method must differ from the signatures of all other methods declared in the same interface, and two methods declared in the same interface may not have signatures that differ solely by ref and out.

The name of a property or event must differ from the names of all other members declared in the same interface.

2) Interface mapping
For purposes of interface mapping, a class member A matches an interface member B when:
•	A and B are methods, and the name, type, and formal parameter lists of A and B are identical.
•	A and B are properties, the name and type of A and B are identical, and A has the same accessors as B.
•	A and B are events, and the name and type of A and B are identical.

NOTE: There is abit more to interface mapping then I thought. Apparently in the CDL methods can implement methods from the interface using this syntax. 
interface IArtist
{
	void Draw();
}
interface ICowboy
{
	void Draw();
}
class CowboyArtist : ICowboy, IArtist
{
	void DrawWeapon() implements ICowboy.Draw;
	void DrawPainting() implements IArtist.Draw;
}
This was not specified in the grammar and I am unsure whether we will support this in Xlang. 

### Enums
1) Enums with an underlying type of UInt32 must carry the FlagsAttribute. Enums with an underlying type of Int32 must not carry the FlagsAttribute.

2) Enums must have public visibility.

3) Versioning:
Enums are additively versionable. Subsequent versions of a given enum may add values (aka named constants). Pre-existing values may not be removed or changed. Enum values optionally carry the VersionAttribute to distinguish when specific values were added to the enum type. Enum values without a VersionAttribute are considered to have the same version value as the enclosing enum type.

### Enum members
1) The constant value for each enum member must be in the range of the underlying type for the enum. The example
enum Color: UInt32
{
	   Red = -1,
	   Green = -2,
	   Blue = -3
}
results in a compile-time error because the constant values -1, -2, and –3 are not in the range of the underlying integral type UInt32.

2) Multiple enum members may share the same associated value. The example
enum Color 
{
	   Red,
	   Green,
	   Blue,
	Max = Blue
}
shows an enum in which two enum members—Blue and Max—have the same associated value.

3) If the declaration of the enum member has a constant-expression initializer, the value of that constant expression, implicitly converted to the underlying type of the enum. 

If the declaration has no initializer, it is set implicity as follows: 
If the enum member is the first enum member declared in the enum type, its associated value is zero.

Otherwise, the associated value of the enum member is obtained by increasing the associated value of the textually preceding enum member by one. This increased value must be within the range of values that can be represented by the underlying type, otherwise a compile-time error occurs.
The example
using System;
enum Color
{
	   Red,
	   Green = 10,
	   Blue
}
The associated values are:
Red = 0
Green = 10
Blue = 11
for the following reasons:
•	the enum member Red is automatically assigned the value zero (since it has no initializer and is the first enum member);
•	the enum member Green is explicitly given the value 10;
•	and the enum member Blue is automatically assigned the value one greater than the member that textually precedes it.
 

The associated value of an enum member may not, directly or indirectly, use the value of its own associated enum member. Other than this circularity restriction, enum member initializers may freely refer to other enum member initializers, regardless of their textual position. Within an enum member initializer, values of other enum members are always treated as having the type of their underlying type, so that casts are not necessary when referring to other enum members. 
The example
enum Circular
{
	   A = B,
	   B
}
results in a compile-time error because the declarations of A and B are circular. A depends on B explicitly, and B depends on A implicitly.

4) The following operators can be used on values of enum types: binary + (§5.4.4), binary   (§5.4.5), ^, &, | (§5.6.2), and ~ (§5.3.3).
### Delegates

### Delegate members