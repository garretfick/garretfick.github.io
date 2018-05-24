---
layout: post
title: Creating OECL IDs
date: 2014-05-19
---

In the last post, we saw that IDs link things together. In practice, you could use anything for the IDs, as long as both the ID and the reference are the same.

## Universally Unique IDs are Important

Just because you can doesn't mean you should. In this case, you really shouldn't and the format specification tells you you shouldn't. In fact, the format specification tells you to make them universally unique. But why?

Two reasons. Let's suppose you get an OECL file from a manufacturer and you import it to your software. The manufacturer now finds a mistake in the file and releases an update and you import the new file to your software. Ideally, it should replace the old definition (or archive it in some way), but to do that, you need to know which items to replace. IDs tell you which items to update, but that only works if the IDs are universally unique.

Or instead, let's suppose that rather than containing all information in a single file, but instead, it is spread over multiple files. The ID reference, if it containes a fully formed URL followed by the file local ID, might give you a way to spread information among multiple documents. A stable ID facilitates linking multiple files together.

There are no products that work like this, and you shouldn't infer that any are in any plans. But, this should tell you why well created IDs are important.

## Creating a Universally Unique ID

IDs in OECL should be unique, but they should also be reproducible for the same component, model, etc. If two people independently create the same component in different software, the component should be assigned the same ID because it is the same component which faciliitates updating components in a database (library). But there is no registration process, so this is not entierly possible.

Developers (or model writers) should a best effort to construct IDs in a consistent manner so that the same component created in the same software will be assigned the same ID. The OECL format describes a recommended way to achieve this.

> To ensure uniqueness, identifierType instances should be written in reverse domain name notation.
>
> The reverse domain name notation should include a company/organization name, a category for the identifier, and a unique name for the item. Items that comply with a published standard, such as should include the standard body, a category for the identifier, and the unique name for the item.

This means the identifier should look like

1. `com.company_name.category_item`
2. `org.standards_body.category.item`

The OECL format description suggests the following identifier categories:

Element	| Category Identifier
--------|--------------------
ComponentBlueprint | `comp`
OrderablePackageConfiguration | `ordpkg`
SymbolBlueprint | `symb`
ModelBlueprint | `modl`
ManufacturerPackage | `mpkg`
PackageBlueprint | `pkg`

Let's look at the [LM7121 from Texas Instruments](http://www.ti.com/product/lm7121) as an example. It has multiple part numbers and it is available in multiple packages.

![](https://s3-us-west-2.amazonaws.com/ficksworkshop/media/blog/creating-oecl-ids/lm7121_parts.png)

The component would have the following IDs

Category            | ID                    | Note
--------------------|--------------------------|--------
ComponentBlueprint  |com.ti.comp.LM7121        | Functionally distinct component.
OrderablePackageConfiguration |	com.ti.ordpgk.LM7121M, com.ti.ordpkg.LM7121M/NOPB, com.ti.ordpkg.LM7121M5 | Different packages that can be ordered. A one-to-one mapping to part numbers.
SymbolBlueprint     |com.ti.symb.opamp_generic | The graphic symbol for schematic capture.
SimulationModelBlueprint | com.ti.modl.LM7171 | A SPICE simultion model.
ManufacturerPackage      | com.ti.mpkg.8SOIC, com.ti.mpgk.5SOT23 | Standard package names from TI.
PackageBlueprint | org.ipc.pkg.X where X is the specific name from IPC-7351 | Standard packages as defined by IPC.