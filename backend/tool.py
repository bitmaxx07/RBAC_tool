xml_data = """
<data>
<operationList>
<operation>
<name>operation-operation1</name>
<type>operation</type>
<domainName>domain1</domainName>
<mother> </mother>
</operation>
</operationList>
<userList>
<user>
<name>user-user1</name>
<type>user</type>
<attribute>google.com</attribute>
<occupied>false</occupied>
<mother>
<item>role-role1</item>
</mother>
</user>
<user>
<name>user-user2</name>
<type>user</type>
<attribute>bing.com</attribute>
<occupied>false</occupied>
<mother>
<item>role-role1</item>
<item>role-role2</item>
</mother>
</user>
<user>
<name>user-user3</name>
<type>user</type>
<attribute>campus.tum.de</attribute>
<occupied>false</occupied>
<mother>
<item>role-role2</item>
</mother>
</user>
</userList>
<roleList>
<role>
<name>role-role1</name>
<type>role</type>
<mother>
<item>operation-operation1</item>
</mother>
</role>
<role>
<name>role-role2</name>
<type>role</type>
<mother>
<item>operation-operation1</item>
</mother>
</role>
</roleList>
<connections>
<connection>
<from>operation-operation1</from>
<to>role-role1</to>
</connection>
<connection>
<from>operation-operation1</from>
<to>role-role2</to>
</connection>
<connection>
<from>role-role1</from>
<to>user-user1</to>
</connection>
<connection>
<from>role-role1</from>
<to>user-user2</to>
</connection>
<connection>
<from>role-role2</from>
<to>user-user2</to>
</connection>
<connection>
<from>role-role2</from>
<to>user-user3</to>
</connection>
</connections>
</data>"""

length_of_xml_data = len(xml_data.encode('utf-8'))

print(length_of_xml_data)
