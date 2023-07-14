from __future__ import annotations

from typing import Dict, List, TYPE_CHECKING


if TYPE_CHECKING:
    from apix.model import *
    from apix.attribute import *


__all__ = [
    'ApixSelect',
]


class ApixSelect:
    model: ApixModel

    def __new__(cls, *args: ApixAttribute):
        return super().__new__(cls)

    def __init__(self, *args: ApixAttribute):
        self.attributes = list(args)

    def __repr__(self) -> str:
        return f'<{self.model.name}:select>'

    @property
    def lookup_attributes(self) -> List[ApixReferenceAttribute | ApixListAttribute]:

        lookup_attributes = []

        for attribute in self.attributes:
            if attribute.lookup_attribute:
                if attribute.lookup_attribute not in lookup_attributes:
                    lookup_attributes.append(attribute.lookup_attribute)

        return lookup_attributes

    @property
    def project_attributes(self) -> List[ApixAttribute]:

        project_attributes = []

        for attribute in self.attributes:
            if attribute.lookup_attribute:
                attribute = attribute.lookup_attribute
            if attribute not in project_attributes:
                project_attributes.append(attribute)

        return project_attributes

    def get_sub_attributes(
            self,
            lookup_attribute: ApixReferenceAttribute | ApixListAttribute,
    ):

        sub_attributes = []

        for attribute in self.attributes:
            if lookup_attribute in attribute.path and lookup_attribute != attribute.path[-1]:
                sub_attributes.append(attribute.sub_attribute)

        return sub_attributes

    def create_lookup(self, lookup_attribute: ApixReferenceAttribute | ApixListAttribute) -> Dict:

        model = lookup_attribute.reference if lookup_attribute.is_reference_attribute else lookup_attribute.attribute.reference
        sub_attributes = self.get_sub_attributes(lookup_attribute)
        select = model.Select(*sub_attributes)

        return {
            '$lookup': {
                'from': model.name,
                'localField': lookup_attribute.path_name,
                'foreignField': '_id',
                'as': lookup_attribute.path_name,
                'pipeline': select.pipeline,
            }
        }

    @staticmethod
    def create_unroll(lookup_attribute: ApixReferenceAttribute) -> Dict:

        return {
            '$set': {
                lookup_attribute.path_name: {
                    '$arrayElemAt': [f'${lookup_attribute.path_name}', 0]
                }
            }
        }

    @property
    def lookups(self) -> List[Dict]:
        return [self.create_lookup(lookup_attribute) for lookup_attribute in self.lookup_attributes]

    @property
    def unrolls(self) -> List[Dict]:
        return [self.create_unroll(lookup_attribute) for lookup_attribute in self.lookup_attributes if lookup_attribute.is_reference_attribute]

    @property
    def project(self) -> List[Dict]:

        project = []

        if self.project_attributes:
            project.append({'$project': {project_attribute.path_name: 1 for project_attribute in self.project_attributes}})

        return project

    @property
    def pipeline(self) -> List[Dict]:
        return self.lookups + self.unrolls + self.project
