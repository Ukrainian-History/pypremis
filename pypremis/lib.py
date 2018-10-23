import xml.etree.ElementTree as ET
from pypremis.factories import XMLNodeFactory
from pypremis.nodes import *


"""
### Classes for general use in pypremis ###

1. **PremisRecord** is a containing class meant to hold nodes
and facilitate writing them to reading and writing serializations.
"""


class NodeSet:
    """
    A utility container class for internal use by PremisRecord. Holds pypremis nodes indexed by identifier.
    The identifier is a string constructed by joining the appropriate PREMIS identifier type and identifier
    value for that node type (e.g. objectIdentifierType and objectIdentifierValue for Object nodes,
    rightsStatementIdentifierType and rightsStatementIdentifierValue for a Rights node, etc.), separated by
    a ':' character.

    The purpose of this subsidiary class is to facilitate the retrieval of nodes by identifier.
    """
    def __init__(self, node_list=None):
        """
        Initializes a NodeSet object from a list of pypremis nodes, if provided.
        Otherwise, returns an empty object.
        """
        self.nodes = {}

        if node_list:
            pass

    def get_nodes(self, identifier=None):
        """
        Return node (or list of nodes) corresponding to a given identifier (or list of identifiers).

        If identifier is None, then return a list of all nodes in the NodeSet.
        """
        identifier_type = type(identifier)
        if identifier_type is str:
            return self.nodes[identifier]
        if identifier_type is list:
            return [self.nodes[key] for key in identifier]
        if identifier is None:
            return self.nodes.values()
        return []  # in the case of a nonsensical identifier, return an empty list

    def append(self, node):
        """
        Append a node to a NodeSet. The identifier of the node being appended is checked against existing
        identifiers in the NodeSet. If the identifier already exists and the objects are equivalent,
        then append_node() returns silently. If the objects are not equivalent, then an IdentifierCollisionError
        exception is thrown.

        That's the plan, at least...
        """
        node_type = type(node)
        if node_type == Object:
            identifier_type = node.get_objectIdentifier(0).get_objectIdentifierType()
            identifier_value = node.get_objectIdentifier(0).get_objectIdentifierValue()
            key = "{}:{}".format(identifier_type, identifier_value)
            self.nodes[key] = node
        if node_type == Event:
            identifier_type = node.get_eventIdentifier(0).get_eventIdentifierType()
            identifier_value = node.get_eventIdentifier(0).get_eventIdentifierValue()
            key = "{}:{}".format(identifier_type, identifier_value)
            self.nodes[key] = node
        if node_type == Agent:
            identifier_type = node.get_agentIdentifier(0).get_agentIdentifierType()
            identifier_value = node.get_agentIdentifier(0).get_agentIdentifierValue()
            key = "{}:{}".format(identifier_type, identifier_value)
            self.nodes[key] = node
        if node_type == Rights:
            identifier_type = node.get_rightsStatementIdentifier(0).get_rightsStatementIdentifierType()
            identifier_value = node.get_rightsStatementIdentifier(0).get_rightsStatementIdentifierValue()
            key = "{}:{}".format(identifier_type, identifier_value)
            self.nodes[key] = node



class PremisRecord(object):
    """
    A class for holding PremisNode objects. Facilitates reading and writing
    to disk

    __Attributes__

    1. objects_list is a list of instances of object nodes
    2. events_list is a list of instances of event nodes
    3. agents_list is a list of instances of agent nodes
    4. rights_list is a list of instances of rights nodes
    5. filepath is a string which correlates to the location on disk
    of a premis.xml file.
    """
    def __init__(self,
                 objects=None, events=None, agents=None, rights=None,
                 frompath=None):
        """
        Initializes a PremisRecord object from either a list of
        pre-existing nodes or an existing xml file on disk. Requires
        one or the other to be supplied on init.

        __KWArgs__

        * objects (list): a list to initially populate objects_list
        * events (list):  a list to initially populate events_list
        * agents (list):  a list to initially populate agents_list
        * rights (list):  a list to initially populate rights_list
        * frompath (list): a string meant to set the location of an originating
        xml file
        """

        if (frompath and (objects or events or agents or rights)) \
                or \
                (not frompath and not (objects or events or agents or rights)):
            raise ValueError("Must supply either a valid file or at least "
                             "one array of valid PREMIS objects.")

        self.events_list = NodeSet()
        self.objects_list = NodeSet()
        self.agents_list = NodeSet()
        self.rights_list = NodeSet()
        self.filepath = None

        if frompath:
            self.filepath = frompath
            self.populate_from_file(XMLNodeFactory)
        else:
            if objects:
                for x in objects:
                    self.add_object(x)
            if events:
                for x in events:
                    self.add_event(x)
            if agents:
                for x in agents:
                    self.add_agent(x)
            if rights:
                for x in rights:
                    self.add_rights(x)

    def __iter__(self):
        """
        Yields each contained node.

        __Returns__

        * (generator): a generator of each node in the record
        """
        for x in self.get_object_list() + self.get_event_list() + \
                self.get_rights_list() + self.get_agent_list():
            yield x

    def __eq__(self, other):
        """
        Computes equality between two PremisRecord objects.

        __Args__

        1. other: an object to compute equality with.

        __Returns__

        * (bool): A boolean denoting equality
        """
        if not isinstance(other, PremisRecord):
            return False
        for x in self:
            if x not in other:
                return False
        for x in other:
            if x not in self:
                return False
        return True

    def add_event(self, event):
        """
        Adds an event node to the event list.

        __Args__

        1. event (PremisNode): an Event PremisNode instance.
        """
        self.events_list.append(event)

    def get_event(self, eventID):
        """
        Returns the event node with the corresponding eventID.

        __Args__

        1. eventID (str): A string which corresponds to one of the
        eventIdentifierValue's specified in an Event PremisNode instance.

        __Returns__

        * (PremisNode or None): an event PremisNode, or None
        """
        pass

    def get_event_list(self):
        """
        Returns a list containing each associated event node.

        __Returns__

        * (list): the self.events_list attribute
        """
        return self.events_list.get_nodes()

    def add_object(self, obj):
        """
        Adds an object node to the object list.

        __Args__

        1. obj (PremisNode): an Object PremisNode instance
        """
        self.objects_list.append(obj)

    def get_object(self, objID):
        """
        Returns the object node with the corresponding objectID

        __Args__

        1. objID (str): A string which corresponds with one of the
        objectIdentifierValue's specified in an Object PremisNode instance

        __Returns__

        * (PremisNode or None): an object PremisNode, or None
        """
        pass

    def get_object_list(self):
        """
        Returns a list containing each object node.

        __Returns__

        * (list): the self.objects_list attribute
        """
        return self.objects_list.get_nodes()

    def add_agent(self, agent):
        """
        Adds an agent node to the agent list.

        __Args__

        1. agent (PremisNode): an Agent PremisNode instance
        """
        self.agents_list.append(agent)

    def get_agent(self, agentID):
        """
        Returns the agent node with the corresponding agentID.

        __Args__

        1. agentID (str): A string which corresponds with one of the
        agentIdentifierValue's specified in an Agent PremisNode instance

        __Returns__

        * (PremisNode or None): an event PremisNode, or None
        """
        pass

    def get_agent_list(self):
        """
        Returns a list containing each agent node.

        __Returns__

        * (list): the self.agents_list attribute
        """
        return self.agents_list.get_nodes()

    def add_rights(self, rights):
        """
        Adds a rights node to the rights list.

        __Args__

        1. rights (PremisNode): a Rights PremisNode instance
        """
        self.rights_list.append(rights)

    def get_rights(self, rightsID):
        """
        Returns the rights node with the corresponding rightsID

        __Args__

        1. rightsID (str): A string which corresponds with one of the
        rightsIdentifierValue's specified in a Rights PremisNode instance.

        __Returns__

        * (PremisNode or None): a rights PremisNode, or None
        """
        pass

    def get_rights_list(self):
        """
        Returns a list containing each rights node.

        __Returns__

        * (list): the self.rights_list attribute
        """
        return self.rights_list.get_nodes()

    def set_filepath(self, filepath):
        """
        Sets the filepath attribute.

        __Args__

        1. filepath (str): A string corresponding to a filepath on disk that specifies
        the location of a pre-existing premis xml record
        """
        self.filepath = filepath

    def get_filepath(self):
        """
        Returns the filepath attribute.

        __Returns__

        * (str): the self.filepath attribute
        """
        return self.filepath

    def validate(self):
        """
        Validates the contained record against the PREMIS specification.

        __Returns__

        * (bool): A bool denoting validity
        """
        pass

    def populate_from_file(self, factory=XMLNodeFactory, filepath=None):
        """
        Populates the object, event, agent, and rights lists from an existing
        premis xml file

        __Args__

        1. factory (cls): A factory class which implements .find_events(),
        .find_agents(), .find_rights, and .find_objects(), which return
        iterators consisting of Event, Agent, Rights, and Object PremisNode
        instances respectively.

        __KWArgs__

        * filepath (str): A string which specifies the location of a serialization
        supported by the given factory class. If not provided the instances
        filepath attribute is assumed.
        """
        if filepath is None:
            if self.get_filepath() is None:
                raise ValueError("No supplied filepath.")
            filepath = self.get_filepath()
        factory = factory(filepath)
        for event in factory.find_events():
            self.add_event(event)
        for agent in factory.find_agents():
            self.add_agent(agent)
        for rights in factory.find_rights():
            self.add_rights(rights)
        for obj in factory.find_objects():
            self.add_object(obj)
        # This fixes a weird bug where the premis xmlns was being written twice
        # in the attributes of the root tag when calling .write_to_file() in
        # cases where extension nodes contain children that are PremisNodes
        ET.register_namespace('premis', "")
        ET.register_namespace('xsi', "")

    def write(self, targetpath, xml_declaration=True,
                      encoding="unicode", method='xml'):
        # Eventually this function might get more complicated and wrap multiple
        # serializers and what not, but for now it's just XML. If you want your
        # code to be rock solid forever use .write_to_file(), it's named so
        # explicitly that even I would have trouble making an argument for
        # changing its functionality.
        """
        Wrap the function with an obnoxiously long name for backwards
        compatability, see comment note above for more info

        __Args__

        1. targetpath (str): a str corresponding to the intended location on disk
        to write the premis xml file to.
        """
        self.write_to_file(targetpath, xml_declaration=xml_declaration,
                           encoding=encoding, method=method)

    def to_tree(self):
        tree = ET.ElementTree(element=ET.Element('premis:premis'))
        root = tree.getroot()
        root.set('xmlns:premis', "http://www.loc.gov/premis/v3")
        root.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
        root.set('version', "3.0")
        for entry in self:
            root.append(entry.toXML())
        return tree

    def to_xml(self, encoding='unicode', method='xml',
               short_empty_elements=True):
        tree = self.to_tree()
        return ET.tostring(tree.getroot(), encoding=encoding,
                           method=method,
                           short_empty_elements=short_empty_elements)

    def write_to_file(self, targetpath, xml_declaration=True,
                      encoding="unicode", method='xml'):
        """
        Writes the contained premis data structure out to disk as the
        specified path as an xml document.

        __Args__

        1. targetpath (str): a str corresponding to the intended location on disk
        to write the premis xml file to.
        """
        tree = self.to_tree()
        tree.write(targetpath,
                   xml_declaration=True,
                   encoding='unicode',
                   method='xml')
