"""
This module contains useful methods for deserializing the AAS meta-model from XML.
"""
from lxml import etree

from . import utils
from aas_class_structure import aas, submodel


def deserialize_asset_information(xml_elem, xml_ns):
    """
    TODO
    :param xml_elem:
    :param xml_ns:
    :return:
    """

    asset_kind_name = xml_elem.find(xml_ns + "assetKind", xml_elem.nsmap).text
    asset_kind = utils.get_text_mapped_name(asset_kind_name, utils.ASSET_KIND_DICT)

    global_asset_id = xml_elem.find(xml_ns + "globalAssetId", xml_elem.nsmap).text

    # TODO

    return aas.AssetInformation(asset_kind=asset_kind, global_asset_id=global_asset_id)


def deserialize_submodel(xml_elem, xml_ns):
    """
    TODO
    :param xml_elem:
    :param xml_ns:
    :return:
    """
    sm_id = utils.get_xml_elem_text(xml_elem, "id", xml_ns)
    sm_kind = utils.get_xml_elem_text(xml_elem, "kind", xml_ns)
    sm_id_short = utils.get_xml_elem_text(xml_elem, "idShort", xml_ns)

    sm_description = utils.get_elem_description(xml_elem, xml_ns)
    sm_administration = utils.get_elem_administration(xml_elem, xml_ns)
    semantic_id = utils.get_elem_reference_text(xml_elem, "semanticId", xml_ns)

    sm_element_list = xml_elem.find(xml_ns + "submodelElements", xml_elem.nsmap)
    sm_elements: set[submodel.SubmodelElement] = set()
    if sm_element_list is not None:
        for sm_elem in sm_element_list:
            sm_elem_obj = deserialize_submodel_element(sm_elem, xml_ns)
            sm_elements.add(sm_elem_obj)

    return submodel.Submodel(id_=sm_id,
                             submodel_element=sm_elements,
                             id_short=sm_id_short,
                             description=sm_description,
                             administration=sm_administration,
                             semantic_id=semantic_id, kind=sm_kind,
                             # TODO (no estan todos)
                             )


def deserialize_submodel_element(xml_elem, xml_ns):
    """
    TODO
    :param xml_elem:
    :param xml_ns:
    :return:
    """
    # First, we get the attributes that all Submodel Elements share
    sm_id_short = utils.get_xml_elem_text(xml_elem, "idShort", xml_ns)
    display_name_elem = sm_id_short  # TODO (for now same as idShort)
    sm_description = utils.get_elem_description(xml_elem, xml_ns)
    semantic_id = utils.get_elem_reference_text(xml_elem, "semanticId", xml_ns)
    qualifiers = utils.get_elem_qualifiers(xml_elem, xml_ns)

    sm_elem_type = etree.QName(xml_elem).localname  # The element type is in the tag

    match sm_elem_type:
        case "dataElement":
            pass
        case "property":
            value_type = utils.get_xml_elem_text(xml_elem, "valueType", xml_ns)
            value = utils.get_xml_elem_text(xml_elem, "value", xml_ns)
            value_id = utils.get_elem_reference_text(xml_elem, "valueId", xml_ns)

            return submodel.Property(id_short=sm_id_short,
                                     value_type=value_type,
                                     value=value,
                                     value_id=value_id,
                                     display_name=display_name_elem,
                                     description=sm_description,
                                     semantic_id=semantic_id,
                                     qualifier=qualifiers,
                                     # TODO (no estan todos)
                                     )
        case "range":
            value_type = utils.get_xml_elem_text(xml_elem, "valueType", xml_ns)
            min_ = utils.get_xml_elem_text(xml_elem, "valueType", xml_ns)
            max_ = utils.get_xml_elem_text(xml_elem, "value", xml_ns)

            return submodel.Range(id_short=sm_id_short,
                                  value_type=value_type,
                                  min_=min_,
                                  max_=max_,
                                  display_name=display_name_elem,
                                  description=sm_description,
                                  semantic_id=semantic_id,
                                  qualifier=qualifiers,
                                  # TODO (no estan todos)
                                  )
        case "blob":
            value_type = utils.get_xml_elem_text(xml_elem, "valueType", xml_ns)
            content_type = utils.get_xml_elem_text(xml_elem, "contentType", xml_ns)

            return submodel.Blob(id_short=sm_id_short,
                                 value_type=value_type,
                                 content_type=content_type,
                                 display_name=display_name_elem,
                                 description=sm_description,
                                 semantic_id=semantic_id,
                                 qualifier=qualifiers,
                                 # TODO (no estan todos)
                                 )
        case "file":
            value = utils.get_xml_elem_text(xml_elem, "value", xml_ns)
            content_type = utils.get_xml_elem_text(xml_elem, "contentType", xml_ns)

            return submodel.File(id_short=sm_id_short,
                                 value_=value,
                                 content_type=content_type,
                                 display_name=display_name_elem,
                                 description=sm_description,
                                 semantic_id=semantic_id,
                                 qualifier=qualifiers,
                                 # TODO (no estan todos)
                                 )
        case "referenceElement":  # TODO, repasarlo porque tiene miga
            value = utils.get_elem_reference_text(xml_elem, "value", xml_ns)

            return submodel.ReferenceElement(id_short=sm_id_short,
                                             value_=value,
                                             display_name=display_name_elem,
                                             description=sm_description,
                                             semantic_id=semantic_id,
                                             qualifier=qualifiers,
                                             # TODO (no estan todos)
                                             )
        case "submodelElementList":
            # TODO
            pass
        case "submodelElementCollection":
            # TODO
            pass
        case "entity":
            entity_type_name = utils.get_xml_elem_text(xml_elem, "entityType", xml_ns)
            entity_type = utils.get_text_mapped_name(entity_type_name, utils.ENTITY_TYPE_DICT)
            global_asset_id = utils.get_xml_elem_text(xml_elem, "globalAssetId", xml_ns)
            specific_asset_id = None  # TODO

            statement = None  # TODO

            return submodel.Entity(id_short=sm_id_short,
                                   entity_type=entity_type,
                                   statement=statement,
                                   global_asset_id=global_asset_id,
                                   specific_asset_id=specific_asset_id,

                                   display_name=display_name_elem,
                                   description=sm_description,
                                   semantic_id=semantic_id,
                                   qualifier=qualifiers,
                                   # TODO (no estan todos)
                                   )
        case "operation":
            input_variable = None  # TODO
            output_variable = None  # TODO
            inoutput_variable = None  # TODO

            return submodel.Operation(id_short=sm_id_short,
                                      input_variable=input_variable,
                                      output_variable=output_variable,
                                      inoutput_variable=inoutput_variable,
                                      display_name=display_name_elem,
                                      description=sm_description,
                                      semantic_id=semantic_id,
                                      qualifier=qualifiers,
                                      # TODO (no estan todos)
                                      )
        case "relationshipElement":
            first = utils.get_elem_reference_text(xml_elem, "first", xml_ns)
            second = utils.get_elem_reference_text(xml_elem, "second", xml_ns)

            return submodel.RelationshipElement(id_short=sm_id_short,
                                                first=first,
                                                second=second,
                                                display_name=display_name_elem,
                                                description=sm_description,
                                                semantic_id=semantic_id,
                                                qualifier=qualifiers,
                                                # TODO (no estan todos)
                                                )


def get_submodel_references(xml_elem, xml_ns):
    """
    TODO
    :param xml_elem:
    :param xml_ns:
    :return:
    """
    sm_references_dict = []
    for ref_elem in xml_elem:
        reference_type = ref_elem.find(xml_ns + "type", ref_elem.nsmap).text
        keys_elem = ref_elem.find(xml_ns + "keys", ref_elem.nsmap)
        key_elem = keys_elem.find(xml_ns + "key", keys_elem.nsmap)
        value = key_elem.find(xml_ns + "value", key_elem.nsmap).text
        sm_references_dict.append({reference_type, value})
    return sm_references_dict