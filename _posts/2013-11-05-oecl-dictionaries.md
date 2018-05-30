---
layout: post
title: OECL Dictionaries and Element Relationships
date: 2013-11-05
---

An OECL file aims to be a complete description of a component or an entire library of components.

## Dictionaries

It does that by defining a series of dictionaries that describe various aspects of components.

Entity | Dictionary
-------|-----------
Components | `ComponentBlueprintDictionary`
Schematic capture graphic symbols | `SymbolBlueprintDictionary`
SPICE simulation models | `SimulationModelBlueprintDictionary`
Manufacturer-defined package names | `ManufacturerPackageDictionary`
Standard packages, also knows as land patterns | `PackageBlueprintDictionary`
Obscolesence and replacements | `StatusDictionary`
Ordering from a supplier | `OrderingInfoDictionary`
Organization of components into a hierarchy | `ComponentCategoryDictionary`

Each of these contains a list of the entities (except for the `ComponentCategoryDictionary`). The `ComponentBlueprintDictionary` contains `ComponentBlueprints`, the `SymbolBlueprintDictionary` contains `SymbolBlueprints`, and so on.

Much of the information about components in general is common. There are probably thousands of operational amplifiers, but most use a common symbol. There are countless components available in the DIP-8 package. The dictionaries facilitate sharing so that the file doesn't repeat common information. There only needs to be one graphic for an operational amplifier and there only needs to be on package for the DIP-8, and so on.

## IDs Link Entities Together

A particular operational amplifier, however, needs to use a particular symbol and a particular package in the file. These are linked together with `id`s. The `ComponentBlueprint` for the operational amplifier will contain referenced to the `id`(s) for the symbol. All items that are referenced by another object contain an `id` attribute. It is quite easy to see which items are referenced by another - just look for the the `id` attribute.

The `SymbolBlueprint` element is referenced by a `ComponentBlueprint`, so it has an `id` attribute, but the `Status` element is not referenced by any, so it does not have an `id` attribute. The `OrderablePackageConfiguration` element is referenced by the `Status` element, so it has an `id` attribute.

Put together, the relationship between thinks looks like the following.

[](/static/img/blog/oecl-dictionaries/oecl_relationships.png)