<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" simplifyLocal="1" minScale="100000000" simplifyMaxScale="1" simplifyAlgorithm="0" version="3.22.7-Białowieża" labelsEnabled="1" styleCategories="AllStyleCategories" symbologyReferenceScale="-1" hasScaleBasedVisibilityFlag="0" simplifyDrawingHints="0" readOnly="0" simplifyDrawingTol="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal endField="data_processamento" durationField="" enabled="0" fixedDuration="0" startExpression="" endExpression="" mode="0" durationUnit="min" startField="" accumulate="0" limitMode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 enableorderby="0" referencescale="-1" type="RuleRenderer" forceraster="0" symbollevels="0">
    <rules key="{700f69b7-78ea-4f16-a052-48c818501aa6}">
      <rule symbol="0" label="Fotos" key="{e87bbde4-939b-4659-8807-9e44978f113e}"/>
      <rule symbol="1" label="Angulos" key="{ec9ca519-1633-4510-b202-7a7271dfbad1}"/>
      <rule symbol="2" key="{64bb7347-c0e6-4415-ba23-772ff451be92}"/>
      <rule symbol="3" label="Ponto" key="{97eb96a9-a1c5-4a93-ac37-bc3717f690ca}"/>
    </rules>
    <symbols>
      <symbol name="0" alpha="1" force_rhr="0" type="marker" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" class="GeometryGenerator" locked="0" pass="0">
          <Option type="Map">
            <Option name="SymbolType" value="Line" type="QString"/>
            <Option name="geometryModifier" value="collect_geometries(&#xd;&#xa;&#x9;make_line(&#xd;&#xa;&#x9;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;&#x9;to_real(&quot;longitude&quot;), to_real(&quot;latitude&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;),&#xd;&#xa;&#x9;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;&#x9;(1e-3 * cos((pi() * 1/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_1&quot;), '_')[1])) + to_real(&quot;longitude&quot;)) ,&#xd;&#xa;&#x9;&#x9;&#x9;(1e-3 * sin((pi() * 1/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_1&quot;), '_')[1])) + to_real(&quot;latitude&quot;)) &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;),&#xd;&#xa;&#x9;make_line(&#xd;&#xa;&#x9;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;&#x9;to_real(&quot;longitude&quot;), to_real(&quot;latitude&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;),&#xd;&#xa;&#x9;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;&#x9;(1e-3 * cos((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_2&quot;), '_')[1])) + to_real(&quot;longitude&quot;)) ,&#xd;&#xa;&#x9;&#x9;&#x9;(1e-3 * sin((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_2&quot;), '_')[1])) + to_real(&quot;latitude&quot;)) &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;),&#xd;&#xa;&#x9;make_line(&#xd;&#xa;&#x9;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;&#x9;to_real(&quot;longitude&quot;), to_real(&quot;latitude&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;),&#xd;&#xa;&#x9;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;&#x9;(1e-3 * cos((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_3&quot;), '_')[1])) + to_real(&quot;longitude&quot;)) ,&#xd;&#xa;&#x9;&#x9;&#x9;(1e-3 * sin((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_3&quot;), '_')[1])) + to_real(&quot;latitude&quot;)) &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;),&#xd;&#xa;&#x9;make_line(&#xd;&#xa;&#x9;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;&#x9;to_real(&quot;longitude&quot;), to_real(&quot;latitude&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;),&#xd;&#xa;&#x9;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;&#x9;(1e-3 * cos((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_4&quot;), '_')[1])) + to_real(&quot;longitude&quot;)) ,&#xd;&#xa;&#x9;&#x9;&#x9;(1e-3 * sin((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_4&quot;), '_')[1])) + to_real(&quot;latitude&quot;)) &#xd;&#xa;&#x9;&#x9;)&#xd;&#xa;&#x9;)&#xd;&#xa;)" type="QString"/>
            <Option name="units" value="MapUnit" type="QString"/>
          </Option>
          <prop k="SymbolType" v="Line"/>
          <prop k="geometryModifier" v="collect_geometries(&#xd;&#xa;&#x9;make_line(&#xd;&#xa;&#x9;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;&#x9;to_real(&quot;longitude&quot;), to_real(&quot;latitude&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;),&#xd;&#xa;&#x9;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;&#x9;(1e-3 * cos((pi() * 1/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_1&quot;), '_')[1])) + to_real(&quot;longitude&quot;)) ,&#xd;&#xa;&#x9;&#x9;&#x9;(1e-3 * sin((pi() * 1/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_1&quot;), '_')[1])) + to_real(&quot;latitude&quot;)) &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;),&#xd;&#xa;&#x9;make_line(&#xd;&#xa;&#x9;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;&#x9;to_real(&quot;longitude&quot;), to_real(&quot;latitude&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;),&#xd;&#xa;&#x9;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;&#x9;(1e-3 * cos((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_2&quot;), '_')[1])) + to_real(&quot;longitude&quot;)) ,&#xd;&#xa;&#x9;&#x9;&#x9;(1e-3 * sin((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_2&quot;), '_')[1])) + to_real(&quot;latitude&quot;)) &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;),&#xd;&#xa;&#x9;make_line(&#xd;&#xa;&#x9;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;&#x9;to_real(&quot;longitude&quot;), to_real(&quot;latitude&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;),&#xd;&#xa;&#x9;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;&#x9;(1e-3 * cos((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_3&quot;), '_')[1])) + to_real(&quot;longitude&quot;)) ,&#xd;&#xa;&#x9;&#x9;&#x9;(1e-3 * sin((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_3&quot;), '_')[1])) + to_real(&quot;latitude&quot;)) &#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;),&#xd;&#xa;&#x9;make_line(&#xd;&#xa;&#x9;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;&#x9;to_real(&quot;longitude&quot;), to_real(&quot;latitude&quot;)&#xd;&#xa;&#x9;&#x9;&#x9;),&#xd;&#xa;&#x9;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;&#x9;(1e-3 * cos((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_4&quot;), '_')[1])) + to_real(&quot;longitude&quot;)) ,&#xd;&#xa;&#x9;&#x9;&#x9;(1e-3 * sin((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_4&quot;), '_')[1])) + to_real(&quot;latitude&quot;)) &#xd;&#xa;&#x9;&#x9;)&#xd;&#xa;&#x9;)&#xd;&#xa;)"/>
          <prop k="units" v="MapUnit"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@0@0" alpha="1" force_rhr="0" type="line" clip_to_extent="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer enabled="1" class="SimpleLine" locked="0" pass="0">
              <Option type="Map">
                <Option name="align_dash_pattern" value="0" type="QString"/>
                <Option name="capstyle" value="square" type="QString"/>
                <Option name="customdash" value="5;2" type="QString"/>
                <Option name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="customdash_unit" value="MM" type="QString"/>
                <Option name="dash_pattern_offset" value="0" type="QString"/>
                <Option name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="dash_pattern_offset_unit" value="MM" type="QString"/>
                <Option name="draw_inside_polygon" value="0" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="line_color" value="255,225,1,255" type="QString"/>
                <Option name="line_style" value="solid" type="QString"/>
                <Option name="line_width" value="1.5" type="QString"/>
                <Option name="line_width_unit" value="MM" type="QString"/>
                <Option name="offset" value="5.55112e-17" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="ring_filter" value="0" type="QString"/>
                <Option name="trim_distance_end" value="0" type="QString"/>
                <Option name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="trim_distance_end_unit" value="MM" type="QString"/>
                <Option name="trim_distance_start" value="0" type="QString"/>
                <Option name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="trim_distance_start_unit" value="MM" type="QString"/>
                <Option name="tweak_dash_pattern_on_corners" value="0" type="QString"/>
                <Option name="use_custom_dash" value="0" type="QString"/>
                <Option name="width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
              </Option>
              <prop k="align_dash_pattern" v="0"/>
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="MM"/>
              <prop k="dash_pattern_offset" v="0"/>
              <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="dash_pattern_offset_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="255,225,1,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="1.5"/>
              <prop k="line_width_unit" v="MM"/>
              <prop k="offset" v="5.55112e-17"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="ring_filter" v="0"/>
              <prop k="trim_distance_end" v="0"/>
              <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="trim_distance_end_unit" v="MM"/>
              <prop k="trim_distance_start" v="0"/>
              <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="trim_distance_start_unit" v="MM"/>
              <prop k="tweak_dash_pattern_on_corners" v="0"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties"/>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="1" alpha="1" force_rhr="0" type="marker" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" class="GeometryGenerator" locked="0" pass="0">
          <Option type="Map">
            <Option name="SymbolType" value="Marker" type="QString"/>
            <Option name="geometryModifier" value="collect_geometries(&#xd;&#xa;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;0.001 * cos((pi() * 1/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_1&quot;), '_')[1])) + to_real(&quot;longitude&quot;),&#xd;&#xa;&#x9;&#x9;0.001 * sin((pi() * 1/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_1&quot;), '_')[1])) + to_real(&quot;latitude&quot;)&#xd;&#xa;&#x9;&#x9;),&#xd;&#xa;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;0.001 * cos((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_2&quot;), '_')[1])) + to_real(&quot;longitude&quot;),&#xd;&#xa;&#x9;&#x9;0.001 * sin((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_2&quot;), '_')[1])) + to_real(&quot;latitude&quot;)&#xd;&#xa;&#x9;&#x9;),&#xd;&#xa;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;0.001 * cos((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_3&quot;), '_')[1])) + to_real(&quot;longitude&quot;),&#xd;&#xa;&#x9;&#x9;0.001 * sin((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_3&quot;), '_')[1])) + to_real(&quot;latitude&quot;)&#xd;&#xa;&#x9;&#x9;),&#xd;&#xa;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;0.001 * cos((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_4&quot;), '_')[1])) + to_real(&quot;longitude&quot;),&#xd;&#xa;&#x9;&#x9;0.001 * sin((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_4&quot;), '_')[1])) + to_real(&quot;latitude&quot;)&#xd;&#xa;&#x9;)&#xd;&#xa;)" type="QString"/>
            <Option name="units" value="MapUnit" type="QString"/>
          </Option>
          <prop k="SymbolType" v="Marker"/>
          <prop k="geometryModifier" v="collect_geometries(&#xd;&#xa;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;0.001 * cos((pi() * 1/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_1&quot;), '_')[1])) + to_real(&quot;longitude&quot;),&#xd;&#xa;&#x9;&#x9;0.001 * sin((pi() * 1/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_1&quot;), '_')[1])) + to_real(&quot;latitude&quot;)&#xd;&#xa;&#x9;&#x9;),&#xd;&#xa;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;0.001 * cos((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_2&quot;), '_')[1])) + to_real(&quot;longitude&quot;),&#xd;&#xa;&#x9;&#x9;0.001 * sin((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_2&quot;), '_')[1])) + to_real(&quot;latitude&quot;)&#xd;&#xa;&#x9;&#x9;),&#xd;&#xa;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;0.001 * cos((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_3&quot;), '_')[1])) + to_real(&quot;longitude&quot;),&#xd;&#xa;&#x9;&#x9;0.001 * sin((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_3&quot;), '_')[1])) + to_real(&quot;latitude&quot;)&#xd;&#xa;&#x9;&#x9;),&#xd;&#xa;&#x9;make_point(&#xd;&#xa;&#x9;&#x9;0.001 * cos((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_4&quot;), '_')[1])) + to_real(&quot;longitude&quot;),&#xd;&#xa;&#x9;&#x9;0.001 * sin((pi() * 5/2) - (pi() / 180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_4&quot;), '_')[1])) + to_real(&quot;latitude&quot;)&#xd;&#xa;&#x9;)&#xd;&#xa;)"/>
          <prop k="units" v="MapUnit"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@1@0" alpha="1" force_rhr="0" type="marker" clip_to_extent="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
              <Option type="Map">
                <Option name="angle" value="0" type="QString"/>
                <Option name="cap_style" value="square" type="QString"/>
                <Option name="color" value="255,255,255,255" type="QString"/>
                <Option name="horizontal_anchor_point" value="1" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="name" value="circle" type="QString"/>
                <Option name="offset" value="0,0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_color" value="0,0,0,255" type="QString"/>
                <Option name="outline_style" value="solid" type="QString"/>
                <Option name="outline_width" value="0.2" type="QString"/>
                <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="outline_width_unit" value="MM" type="QString"/>
                <Option name="scale_method" value="area" type="QString"/>
                <Option name="size" value="4.2" type="QString"/>
                <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="size_unit" value="MM" type="QString"/>
                <Option name="vertical_anchor_point" value="1" type="QString"/>
              </Option>
              <prop k="angle" v="0"/>
              <prop k="cap_style" v="square"/>
              <prop k="color" v="255,255,255,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="circle"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="0,0,0,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0.2"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="area"/>
              <prop k="size" v="4.2"/>
              <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties"/>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
            <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
              <Option type="Map">
                <Option name="angle" value="0" type="QString"/>
                <Option name="cap_style" value="square" type="QString"/>
                <Option name="color" value="0,0,0,255" type="QString"/>
                <Option name="horizontal_anchor_point" value="1" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="name" value="circle" type="QString"/>
                <Option name="offset" value="0,0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="outline_color" value="0,0,0,255" type="QString"/>
                <Option name="outline_style" value="solid" type="QString"/>
                <Option name="outline_width" value="0.4" type="QString"/>
                <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="outline_width_unit" value="MM" type="QString"/>
                <Option name="scale_method" value="area" type="QString"/>
                <Option name="size" value="0.91875" type="QString"/>
                <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="size_unit" value="MM" type="QString"/>
                <Option name="vertical_anchor_point" value="1" type="QString"/>
              </Option>
              <prop k="angle" v="0"/>
              <prop k="cap_style" v="square"/>
              <prop k="color" v="0,0,0,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="circle"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="0,0,0,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0.4"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="area"/>
              <prop k="size" v="0.91875"/>
              <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties"/>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="2" alpha="1" force_rhr="0" type="marker" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" class="GeometryGenerator" locked="0" pass="0">
          <Option type="Map">
            <Option name="SymbolType" value="Line" type="QString"/>
            <Option name="geometryModifier" value="make_line(make_point(&quot;longitude&quot;, &quot;latitude&quot;), make_point(&quot;longitude_planejada&quot;, &quot;latitude_planejada&quot;))" type="QString"/>
            <Option name="units" value="MapUnit" type="QString"/>
          </Option>
          <prop k="SymbolType" v="Line"/>
          <prop k="geometryModifier" v="make_line(make_point(&quot;longitude&quot;, &quot;latitude&quot;), make_point(&quot;longitude_planejada&quot;, &quot;latitude_planejada&quot;))"/>
          <prop k="units" v="MapUnit"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <symbol name="@2@0" alpha="1" force_rhr="0" type="line" clip_to_extent="1">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
            <layer enabled="1" class="SimpleLine" locked="0" pass="0">
              <Option type="Map">
                <Option name="align_dash_pattern" value="0" type="QString"/>
                <Option name="capstyle" value="square" type="QString"/>
                <Option name="customdash" value="5;2" type="QString"/>
                <Option name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="customdash_unit" value="MM" type="QString"/>
                <Option name="dash_pattern_offset" value="0" type="QString"/>
                <Option name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="dash_pattern_offset_unit" value="MM" type="QString"/>
                <Option name="draw_inside_polygon" value="0" type="QString"/>
                <Option name="joinstyle" value="bevel" type="QString"/>
                <Option name="line_color" value="255,86,1,255" type="QString"/>
                <Option name="line_style" value="solid" type="QString"/>
                <Option name="line_width" value="0.75" type="QString"/>
                <Option name="line_width_unit" value="MM" type="QString"/>
                <Option name="offset" value="0" type="QString"/>
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="offset_unit" value="MM" type="QString"/>
                <Option name="ring_filter" value="0" type="QString"/>
                <Option name="trim_distance_end" value="0" type="QString"/>
                <Option name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="trim_distance_end_unit" value="MM" type="QString"/>
                <Option name="trim_distance_start" value="0" type="QString"/>
                <Option name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                <Option name="trim_distance_start_unit" value="MM" type="QString"/>
                <Option name="tweak_dash_pattern_on_corners" value="0" type="QString"/>
                <Option name="use_custom_dash" value="0" type="QString"/>
                <Option name="width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
              </Option>
              <prop k="align_dash_pattern" v="0"/>
              <prop k="capstyle" v="square"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="customdash_unit" v="MM"/>
              <prop k="dash_pattern_offset" v="0"/>
              <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="dash_pattern_offset_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="line_color" v="255,86,1,255"/>
              <prop k="line_style" v="solid"/>
              <prop k="line_width" v="0.75"/>
              <prop k="line_width_unit" v="MM"/>
              <prop k="offset" v="0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="ring_filter" v="0"/>
              <prop k="trim_distance_end" v="0"/>
              <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="trim_distance_end_unit" v="MM"/>
              <prop k="trim_distance_start" v="0"/>
              <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="trim_distance_start_unit" v="MM"/>
              <prop k="tweak_dash_pattern_on_corners" v="0"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString"/>
                  <Option name="properties"/>
                  <Option name="type" value="collection" type="QString"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol name="3" alpha="1" force_rhr="0" type="marker" clip_to_extent="1">
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties"/>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
        <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
          <Option type="Map">
            <Option name="angle" value="0" type="QString"/>
            <Option name="cap_style" value="square" type="QString"/>
            <Option name="color" value="0,0,0,255" type="QString"/>
            <Option name="horizontal_anchor_point" value="1" type="QString"/>
            <Option name="joinstyle" value="bevel" type="QString"/>
            <Option name="name" value="triangle" type="QString"/>
            <Option name="offset" value="0,0" type="QString"/>
            <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="offset_unit" value="MM" type="QString"/>
            <Option name="outline_color" value="50,87,128,255" type="QString"/>
            <Option name="outline_style" value="solid" type="QString"/>
            <Option name="outline_width" value="0.4" type="QString"/>
            <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="outline_width_unit" value="MM" type="QString"/>
            <Option name="scale_method" value="diameter" type="QString"/>
            <Option name="size" value="6" type="QString"/>
            <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            <Option name="size_unit" value="MM" type="QString"/>
            <Option name="vertical_anchor_point" value="1" type="QString"/>
          </Option>
          <prop k="angle" v="0"/>
          <prop k="cap_style" v="square"/>
          <prop k="color" v="0,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="triangle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="50,87,128,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.4"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="6"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <labeling type="rule-based">
    <rules key="{9f7464c0-e244-49af-abdf-105a359b3f15}">
      <rule key="{16349559-2e85-4eb0-bbe9-9cc860d1cd0d}">
        <settings calloutType="simple">
          <text-style legendString="Aa" fontItalic="0" capitalization="0" fontKerning="1" textOpacity="1" fontSize="12" fontSizeMapUnitScale="3x:0,0,0,0,0,0" textColor="19,255,15,255" allowHtml="0" isExpression="0" fieldName="cod_ponto" useSubstitutions="0" blendMode="0" previewBkgrdColor="255,255,255,255" namedStyle="Regular" fontWordSpacing="0.1875" multilineHeight="1" fontFamily="Open Sans" fontStrikeout="0" fontLetterSpacing="0.5" fontSizeUnit="Point" textOrientation="horizontal" fontUnderline="0" fontWeight="50">
            <families/>
            <text-buffer bufferColor="0,0,0,255" bufferOpacity="1" bufferSizeUnits="MM" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128" bufferDraw="1" bufferBlendMode="0" bufferSize="1" bufferNoFill="1"/>
            <text-mask maskType="0" maskOpacity="1" maskEnabled="0" maskedSymbolLayers="" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskJoinStyle="128" maskSizeUnits="MM" maskSize="0"/>
            <background shapeOffsetX="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOpacity="1" shapeRadiiUnit="Point" shapeFillColor="255,255,255,255" shapeRotation="0" shapeType="0" shapeSizeY="0" shapeBorderColor="128,128,128,255" shapeRotationType="0" shapeOffsetUnit="Point" shapeSizeUnit="Point" shapeSizeX="0" shapeJoinStyle="64" shapeRadiiX="0" shapeRadiiY="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetY="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeBlendMode="0" shapeSVGFile="" shapeSizeType="0" shapeBorderWidth="0" shapeDraw="0" shapeBorderWidthUnit="Point">
              <symbol name="markerSymbol" alpha="1" force_rhr="0" type="marker" clip_to_extent="1">
                <data_defined_properties>
                  <Option type="Map">
                    <Option name="name" value="" type="QString"/>
                    <Option name="properties"/>
                    <Option name="type" value="collection" type="QString"/>
                  </Option>
                </data_defined_properties>
                <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
                  <Option type="Map">
                    <Option name="angle" value="0" type="QString"/>
                    <Option name="cap_style" value="square" type="QString"/>
                    <Option name="color" value="232,113,141,255" type="QString"/>
                    <Option name="horizontal_anchor_point" value="1" type="QString"/>
                    <Option name="joinstyle" value="bevel" type="QString"/>
                    <Option name="name" value="circle" type="QString"/>
                    <Option name="offset" value="0,0" type="QString"/>
                    <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="offset_unit" value="MM" type="QString"/>
                    <Option name="outline_color" value="35,35,35,255" type="QString"/>
                    <Option name="outline_style" value="solid" type="QString"/>
                    <Option name="outline_width" value="0" type="QString"/>
                    <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="outline_width_unit" value="MM" type="QString"/>
                    <Option name="scale_method" value="diameter" type="QString"/>
                    <Option name="size" value="2" type="QString"/>
                    <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="size_unit" value="MM" type="QString"/>
                    <Option name="vertical_anchor_point" value="1" type="QString"/>
                  </Option>
                  <prop k="angle" v="0"/>
                  <prop k="cap_style" v="square"/>
                  <prop k="color" v="232,113,141,255"/>
                  <prop k="horizontal_anchor_point" v="1"/>
                  <prop k="joinstyle" v="bevel"/>
                  <prop k="name" v="circle"/>
                  <prop k="offset" v="0,0"/>
                  <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="offset_unit" v="MM"/>
                  <prop k="outline_color" v="35,35,35,255"/>
                  <prop k="outline_style" v="solid"/>
                  <prop k="outline_width" v="0"/>
                  <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="outline_width_unit" v="MM"/>
                  <prop k="scale_method" v="diameter"/>
                  <prop k="size" v="2"/>
                  <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="size_unit" v="MM"/>
                  <prop k="vertical_anchor_point" v="1"/>
                  <data_defined_properties>
                    <Option type="Map">
                      <Option name="name" value="" type="QString"/>
                      <Option name="properties"/>
                      <Option name="type" value="collection" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
              <symbol name="fillSymbol" alpha="1" force_rhr="0" type="fill" clip_to_extent="1">
                <data_defined_properties>
                  <Option type="Map">
                    <Option name="name" value="" type="QString"/>
                    <Option name="properties"/>
                    <Option name="type" value="collection" type="QString"/>
                  </Option>
                </data_defined_properties>
                <layer enabled="1" class="SimpleFill" locked="0" pass="0">
                  <Option type="Map">
                    <Option name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="color" value="255,255,255,255" type="QString"/>
                    <Option name="joinstyle" value="bevel" type="QString"/>
                    <Option name="offset" value="0,0" type="QString"/>
                    <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="offset_unit" value="MM" type="QString"/>
                    <Option name="outline_color" value="128,128,128,255" type="QString"/>
                    <Option name="outline_style" value="no" type="QString"/>
                    <Option name="outline_width" value="0" type="QString"/>
                    <Option name="outline_width_unit" value="Point" type="QString"/>
                    <Option name="style" value="solid" type="QString"/>
                  </Option>
                  <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="color" v="255,255,255,255"/>
                  <prop k="joinstyle" v="bevel"/>
                  <prop k="offset" v="0,0"/>
                  <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="offset_unit" v="MM"/>
                  <prop k="outline_color" v="128,128,128,255"/>
                  <prop k="outline_style" v="no"/>
                  <prop k="outline_width" v="0"/>
                  <prop k="outline_width_unit" v="Point"/>
                  <prop k="style" v="solid"/>
                  <data_defined_properties>
                    <Option type="Map">
                      <Option name="name" value="" type="QString"/>
                      <Option name="properties"/>
                      <Option name="type" value="collection" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </background>
            <shadow shadowUnder="0" shadowOffsetDist="1" shadowRadiusAlphaOnly="0" shadowDraw="0" shadowOffsetGlobal="1" shadowRadius="1.5" shadowOffsetUnit="MM" shadowScale="100" shadowOffsetAngle="135" shadowColor="0,0,0,255" shadowOpacity="0.69999999999999996" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusUnit="MM" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowBlendMode="6"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format useMaxLineLengthForAutoWrap="1" addDirectionSymbol="0" rightDirectionSymbol=">" reverseDirectionSymbol="0" decimals="3" placeDirectionSymbol="0" plussign="0" wrapChar="" formatNumbers="0" autoWrapLength="0" multilineAlign="3" leftDirectionSymbol="&lt;"/>
          <placement placement="6" polygonPlacementFlags="2" preserveRotation="1" repeatDistance="0" xOffset="0" dist="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" yOffset="0" centroidWhole="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MM" rotationUnit="AngleDegrees" geometryGeneratorType="PointGeometry" maxCurvedCharAngleIn="25" lineAnchorType="0" lineAnchorClipping="0" rotationAngle="0" centroidInside="0" layerType="PointGeometry" geometryGeneratorEnabled="0" priority="5" quadOffset="4" maxCurvedCharAngleOut="-25" geometryGenerator="" distMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0" overrunDistanceUnit="MM" placementFlags="10" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" distUnits="MM" repeatDistanceUnits="MM" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" lineAnchorPercent="0.5" offsetType="1" overrunDistance="0"/>
          <rendering fontMinPixelSize="3" upsidedownLabels="0" fontMaxPixelSize="10000" limitNumLabels="0" scaleMin="0" minFeatureSize="0" maxNumLabels="2000" drawLabels="1" obstacleFactor="1" obstacle="1" fontLimitPixelSize="0" obstacleType="1" unplacedVisibility="0" scaleMax="0" labelPerPart="0" scaleVisibility="0" zIndex="0" mergeLines="0" displayAll="0"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="PositionX" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="0.001 + &quot;longitude&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="PositionY" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="&quot;latitude&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option name="anchorPoint" value="pole_of_inaccessibility" type="QString"/>
              <Option name="blendMode" value="0" type="int"/>
              <Option name="ddProperties" type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
              <Option name="drawToAllParts" value="false" type="bool"/>
              <Option name="enabled" value="0" type="QString"/>
              <Option name="labelAnchorPoint" value="point_on_exterior" type="QString"/>
              <Option name="lineSymbol" value="&lt;symbol name=&quot;symbol&quot; alpha=&quot;1&quot; force_rhr=&quot;0&quot; type=&quot;line&quot; clip_to_extent=&quot;1&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer enabled=&quot;1&quot; class=&quot;SimpleLine&quot; locked=&quot;0&quot; pass=&quot;0&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;align_dash_pattern&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;capstyle&quot; value=&quot;square&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash&quot; value=&quot;5;2&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;draw_inside_polygon&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;joinstyle&quot; value=&quot;bevel&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_color&quot; value=&quot;60,60,60,255&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_style&quot; value=&quot;solid&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_width&quot; value=&quot;0.3&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_width_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;ring_filter&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;tweak_dash_pattern_on_corners&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;use_custom_dash&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;width_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_end_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;trim_distance_start&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_start_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_start_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString"/>
              <Option name="minLength" value="0" type="double"/>
              <Option name="minLengthMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="minLengthUnit" value="MM" type="QString"/>
              <Option name="offsetFromAnchor" value="0" type="double"/>
              <Option name="offsetFromAnchorMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromAnchorUnit" value="MM" type="QString"/>
              <Option name="offsetFromLabel" value="0" type="double"/>
              <Option name="offsetFromLabelMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromLabelUnit" value="MM" type="QString"/>
            </Option>
          </callout>
        </settings>
      </rule>
      <rule key="{59f7a827-0a04-4008-9643-34f57cd6d2a1}">
        <settings calloutType="simple">
          <text-style legendString="Aa" fontItalic="0" capitalization="0" fontKerning="1" textOpacity="1" fontSize="12" fontSizeMapUnitScale="3x:0,0,0,0,0,0" textColor="1,255,35,255" allowHtml="0" isExpression="1" fieldName="string_to_array(file_name(&quot;endereco_imagem_lateral_1&quot;), '_')[1]" useSubstitutions="0" blendMode="0" previewBkgrdColor="255,255,255,255" namedStyle="Regular" fontWordSpacing="0" multilineHeight="1" fontFamily="Open Sans" fontStrikeout="0" fontLetterSpacing="0" fontSizeUnit="Point" textOrientation="horizontal" fontUnderline="0" fontWeight="50">
            <families/>
            <text-buffer bufferColor="0,0,0,255" bufferOpacity="1" bufferSizeUnits="MM" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128" bufferDraw="1" bufferBlendMode="0" bufferSize="1" bufferNoFill="1"/>
            <text-mask maskType="0" maskOpacity="1" maskEnabled="0" maskedSymbolLayers="" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskJoinStyle="128" maskSizeUnits="MM" maskSize="0"/>
            <background shapeOffsetX="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOpacity="1" shapeRadiiUnit="Point" shapeFillColor="255,255,255,255" shapeRotation="0" shapeType="0" shapeSizeY="0" shapeBorderColor="128,128,128,255" shapeRotationType="0" shapeOffsetUnit="Point" shapeSizeUnit="Point" shapeSizeX="0" shapeJoinStyle="64" shapeRadiiX="0" shapeRadiiY="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetY="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeBlendMode="0" shapeSVGFile="" shapeSizeType="0" shapeBorderWidth="0" shapeDraw="0" shapeBorderWidthUnit="Point">
              <symbol name="markerSymbol" alpha="1" force_rhr="0" type="marker" clip_to_extent="1">
                <data_defined_properties>
                  <Option type="Map">
                    <Option name="name" value="" type="QString"/>
                    <Option name="properties"/>
                    <Option name="type" value="collection" type="QString"/>
                  </Option>
                </data_defined_properties>
                <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
                  <Option type="Map">
                    <Option name="angle" value="0" type="QString"/>
                    <Option name="cap_style" value="square" type="QString"/>
                    <Option name="color" value="232,113,141,255" type="QString"/>
                    <Option name="horizontal_anchor_point" value="1" type="QString"/>
                    <Option name="joinstyle" value="bevel" type="QString"/>
                    <Option name="name" value="circle" type="QString"/>
                    <Option name="offset" value="0,0" type="QString"/>
                    <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="offset_unit" value="MM" type="QString"/>
                    <Option name="outline_color" value="35,35,35,255" type="QString"/>
                    <Option name="outline_style" value="solid" type="QString"/>
                    <Option name="outline_width" value="0" type="QString"/>
                    <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="outline_width_unit" value="MM" type="QString"/>
                    <Option name="scale_method" value="diameter" type="QString"/>
                    <Option name="size" value="2" type="QString"/>
                    <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="size_unit" value="MM" type="QString"/>
                    <Option name="vertical_anchor_point" value="1" type="QString"/>
                  </Option>
                  <prop k="angle" v="0"/>
                  <prop k="cap_style" v="square"/>
                  <prop k="color" v="232,113,141,255"/>
                  <prop k="horizontal_anchor_point" v="1"/>
                  <prop k="joinstyle" v="bevel"/>
                  <prop k="name" v="circle"/>
                  <prop k="offset" v="0,0"/>
                  <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="offset_unit" v="MM"/>
                  <prop k="outline_color" v="35,35,35,255"/>
                  <prop k="outline_style" v="solid"/>
                  <prop k="outline_width" v="0"/>
                  <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="outline_width_unit" v="MM"/>
                  <prop k="scale_method" v="diameter"/>
                  <prop k="size" v="2"/>
                  <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="size_unit" v="MM"/>
                  <prop k="vertical_anchor_point" v="1"/>
                  <data_defined_properties>
                    <Option type="Map">
                      <Option name="name" value="" type="QString"/>
                      <Option name="properties"/>
                      <Option name="type" value="collection" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
              <symbol name="fillSymbol" alpha="1" force_rhr="0" type="fill" clip_to_extent="1">
                <data_defined_properties>
                  <Option type="Map">
                    <Option name="name" value="" type="QString"/>
                    <Option name="properties"/>
                    <Option name="type" value="collection" type="QString"/>
                  </Option>
                </data_defined_properties>
                <layer enabled="1" class="SimpleFill" locked="0" pass="0">
                  <Option type="Map">
                    <Option name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="color" value="255,255,255,255" type="QString"/>
                    <Option name="joinstyle" value="bevel" type="QString"/>
                    <Option name="offset" value="0,0" type="QString"/>
                    <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="offset_unit" value="MM" type="QString"/>
                    <Option name="outline_color" value="128,128,128,255" type="QString"/>
                    <Option name="outline_style" value="no" type="QString"/>
                    <Option name="outline_width" value="0" type="QString"/>
                    <Option name="outline_width_unit" value="Point" type="QString"/>
                    <Option name="style" value="solid" type="QString"/>
                  </Option>
                  <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="color" v="255,255,255,255"/>
                  <prop k="joinstyle" v="bevel"/>
                  <prop k="offset" v="0,0"/>
                  <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="offset_unit" v="MM"/>
                  <prop k="outline_color" v="128,128,128,255"/>
                  <prop k="outline_style" v="no"/>
                  <prop k="outline_width" v="0"/>
                  <prop k="outline_width_unit" v="Point"/>
                  <prop k="style" v="solid"/>
                  <data_defined_properties>
                    <Option type="Map">
                      <Option name="name" value="" type="QString"/>
                      <Option name="properties"/>
                      <Option name="type" value="collection" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </background>
            <shadow shadowUnder="0" shadowOffsetDist="1" shadowRadiusAlphaOnly="0" shadowDraw="0" shadowOffsetGlobal="1" shadowRadius="1.5" shadowOffsetUnit="MM" shadowScale="100" shadowOffsetAngle="135" shadowColor="0,0,0,255" shadowOpacity="0.69999999999999996" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusUnit="MM" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowBlendMode="6"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format useMaxLineLengthForAutoWrap="1" addDirectionSymbol="0" rightDirectionSymbol=">" reverseDirectionSymbol="0" decimals="3" placeDirectionSymbol="0" plussign="0" wrapChar="" formatNumbers="0" autoWrapLength="0" multilineAlign="3" leftDirectionSymbol="&lt;"/>
          <placement placement="6" polygonPlacementFlags="2" preserveRotation="1" repeatDistance="0" xOffset="0" dist="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" yOffset="0" centroidWhole="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MM" rotationUnit="AngleDegrees" geometryGeneratorType="PointGeometry" maxCurvedCharAngleIn="25" lineAnchorType="0" lineAnchorClipping="0" rotationAngle="0" centroidInside="0" layerType="PointGeometry" geometryGeneratorEnabled="0" priority="5" quadOffset="4" maxCurvedCharAngleOut="-25" geometryGenerator="" distMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0" overrunDistanceUnit="MM" placementFlags="10" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" distUnits="MapUnit" repeatDistanceUnits="MM" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" lineAnchorPercent="0.5" offsetType="1" overrunDistance="0"/>
          <rendering fontMinPixelSize="3" upsidedownLabels="0" fontMaxPixelSize="10000" limitNumLabels="0" scaleMin="0" minFeatureSize="0" maxNumLabels="2000" drawLabels="1" obstacleFactor="1" obstacle="1" fontLimitPixelSize="0" obstacleType="1" unplacedVisibility="0" scaleMax="0" labelPerPart="0" scaleVisibility="0" zIndex="0" mergeLines="0" displayAll="0"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="LabelRotation" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="180" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="PositionX" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="0.00125 * cos(pi()/2 - (pi()/180)*to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_1&quot;), '_')[1]))+&quot;longitude&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="PositionY" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="0.00125 * sin(pi()/2 - (pi()/180) * to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_1&quot;), '_')[1]))+&quot;latitude&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option name="anchorPoint" value="pole_of_inaccessibility" type="QString"/>
              <Option name="blendMode" value="0" type="int"/>
              <Option name="ddProperties" type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
              <Option name="drawToAllParts" value="false" type="bool"/>
              <Option name="enabled" value="0" type="QString"/>
              <Option name="labelAnchorPoint" value="point_on_exterior" type="QString"/>
              <Option name="lineSymbol" value="&lt;symbol name=&quot;symbol&quot; alpha=&quot;1&quot; force_rhr=&quot;0&quot; type=&quot;line&quot; clip_to_extent=&quot;1&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer enabled=&quot;1&quot; class=&quot;SimpleLine&quot; locked=&quot;0&quot; pass=&quot;0&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;align_dash_pattern&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;capstyle&quot; value=&quot;square&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash&quot; value=&quot;5;2&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;draw_inside_polygon&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;joinstyle&quot; value=&quot;bevel&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_color&quot; value=&quot;60,60,60,255&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_style&quot; value=&quot;solid&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_width&quot; value=&quot;0.3&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_width_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;ring_filter&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;tweak_dash_pattern_on_corners&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;use_custom_dash&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;width_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_end_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;trim_distance_start&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_start_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_start_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString"/>
              <Option name="minLength" value="0" type="double"/>
              <Option name="minLengthMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="minLengthUnit" value="MM" type="QString"/>
              <Option name="offsetFromAnchor" value="0" type="double"/>
              <Option name="offsetFromAnchorMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromAnchorUnit" value="MM" type="QString"/>
              <Option name="offsetFromLabel" value="0" type="double"/>
              <Option name="offsetFromLabelMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromLabelUnit" value="MM" type="QString"/>
            </Option>
          </callout>
        </settings>
      </rule>
      <rule key="{72eed012-31f3-4ac8-831b-b721687c1832}">
        <settings calloutType="simple">
          <text-style legendString="Aa" fontItalic="0" capitalization="0" fontKerning="1" textOpacity="1" fontSize="12" fontSizeMapUnitScale="3x:0,0,0,0,0,0" textColor="1,255,18,255" allowHtml="0" isExpression="1" fieldName="string_to_array(file_name(&quot;endereco_imagem_lateral_2&quot;), '_')[1]" useSubstitutions="0" blendMode="0" previewBkgrdColor="255,255,255,255" namedStyle="Regular" fontWordSpacing="0" multilineHeight="1" fontFamily="Open Sans" fontStrikeout="0" fontLetterSpacing="0" fontSizeUnit="Point" textOrientation="horizontal" fontUnderline="0" fontWeight="50">
            <families/>
            <text-buffer bufferColor="0,0,0,255" bufferOpacity="1" bufferSizeUnits="MM" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128" bufferDraw="1" bufferBlendMode="0" bufferSize="1" bufferNoFill="1"/>
            <text-mask maskType="0" maskOpacity="1" maskEnabled="0" maskedSymbolLayers="" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskJoinStyle="128" maskSizeUnits="MM" maskSize="0"/>
            <background shapeOffsetX="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOpacity="1" shapeRadiiUnit="Point" shapeFillColor="255,255,255,255" shapeRotation="0" shapeType="0" shapeSizeY="0" shapeBorderColor="128,128,128,255" shapeRotationType="0" shapeOffsetUnit="Point" shapeSizeUnit="Point" shapeSizeX="0" shapeJoinStyle="64" shapeRadiiX="0" shapeRadiiY="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetY="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeBlendMode="0" shapeSVGFile="" shapeSizeType="0" shapeBorderWidth="0" shapeDraw="0" shapeBorderWidthUnit="Point">
              <symbol name="markerSymbol" alpha="1" force_rhr="0" type="marker" clip_to_extent="1">
                <data_defined_properties>
                  <Option type="Map">
                    <Option name="name" value="" type="QString"/>
                    <Option name="properties"/>
                    <Option name="type" value="collection" type="QString"/>
                  </Option>
                </data_defined_properties>
                <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
                  <Option type="Map">
                    <Option name="angle" value="0" type="QString"/>
                    <Option name="cap_style" value="square" type="QString"/>
                    <Option name="color" value="232,113,141,255" type="QString"/>
                    <Option name="horizontal_anchor_point" value="1" type="QString"/>
                    <Option name="joinstyle" value="bevel" type="QString"/>
                    <Option name="name" value="circle" type="QString"/>
                    <Option name="offset" value="0,0" type="QString"/>
                    <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="offset_unit" value="MM" type="QString"/>
                    <Option name="outline_color" value="35,35,35,255" type="QString"/>
                    <Option name="outline_style" value="solid" type="QString"/>
                    <Option name="outline_width" value="0" type="QString"/>
                    <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="outline_width_unit" value="MM" type="QString"/>
                    <Option name="scale_method" value="diameter" type="QString"/>
                    <Option name="size" value="2" type="QString"/>
                    <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="size_unit" value="MM" type="QString"/>
                    <Option name="vertical_anchor_point" value="1" type="QString"/>
                  </Option>
                  <prop k="angle" v="0"/>
                  <prop k="cap_style" v="square"/>
                  <prop k="color" v="232,113,141,255"/>
                  <prop k="horizontal_anchor_point" v="1"/>
                  <prop k="joinstyle" v="bevel"/>
                  <prop k="name" v="circle"/>
                  <prop k="offset" v="0,0"/>
                  <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="offset_unit" v="MM"/>
                  <prop k="outline_color" v="35,35,35,255"/>
                  <prop k="outline_style" v="solid"/>
                  <prop k="outline_width" v="0"/>
                  <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="outline_width_unit" v="MM"/>
                  <prop k="scale_method" v="diameter"/>
                  <prop k="size" v="2"/>
                  <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="size_unit" v="MM"/>
                  <prop k="vertical_anchor_point" v="1"/>
                  <data_defined_properties>
                    <Option type="Map">
                      <Option name="name" value="" type="QString"/>
                      <Option name="properties"/>
                      <Option name="type" value="collection" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
              <symbol name="fillSymbol" alpha="1" force_rhr="0" type="fill" clip_to_extent="1">
                <data_defined_properties>
                  <Option type="Map">
                    <Option name="name" value="" type="QString"/>
                    <Option name="properties"/>
                    <Option name="type" value="collection" type="QString"/>
                  </Option>
                </data_defined_properties>
                <layer enabled="1" class="SimpleFill" locked="0" pass="0">
                  <Option type="Map">
                    <Option name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="color" value="255,255,255,255" type="QString"/>
                    <Option name="joinstyle" value="bevel" type="QString"/>
                    <Option name="offset" value="0,0" type="QString"/>
                    <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="offset_unit" value="MM" type="QString"/>
                    <Option name="outline_color" value="128,128,128,255" type="QString"/>
                    <Option name="outline_style" value="no" type="QString"/>
                    <Option name="outline_width" value="0" type="QString"/>
                    <Option name="outline_width_unit" value="Point" type="QString"/>
                    <Option name="style" value="solid" type="QString"/>
                  </Option>
                  <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="color" v="255,255,255,255"/>
                  <prop k="joinstyle" v="bevel"/>
                  <prop k="offset" v="0,0"/>
                  <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="offset_unit" v="MM"/>
                  <prop k="outline_color" v="128,128,128,255"/>
                  <prop k="outline_style" v="no"/>
                  <prop k="outline_width" v="0"/>
                  <prop k="outline_width_unit" v="Point"/>
                  <prop k="style" v="solid"/>
                  <data_defined_properties>
                    <Option type="Map">
                      <Option name="name" value="" type="QString"/>
                      <Option name="properties"/>
                      <Option name="type" value="collection" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </background>
            <shadow shadowUnder="0" shadowOffsetDist="1" shadowRadiusAlphaOnly="0" shadowDraw="0" shadowOffsetGlobal="1" shadowRadius="1.5" shadowOffsetUnit="MM" shadowScale="100" shadowOffsetAngle="135" shadowColor="0,0,0,255" shadowOpacity="0.69999999999999996" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusUnit="MM" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowBlendMode="6"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format useMaxLineLengthForAutoWrap="1" addDirectionSymbol="0" rightDirectionSymbol=">" reverseDirectionSymbol="0" decimals="3" placeDirectionSymbol="0" plussign="0" wrapChar="" formatNumbers="0" autoWrapLength="0" multilineAlign="3" leftDirectionSymbol="&lt;"/>
          <placement placement="6" polygonPlacementFlags="2" preserveRotation="1" repeatDistance="0" xOffset="0" dist="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" yOffset="0" centroidWhole="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MM" rotationUnit="AngleDegrees" geometryGeneratorType="PointGeometry" maxCurvedCharAngleIn="25" lineAnchorType="0" lineAnchorClipping="0" rotationAngle="0" centroidInside="0" layerType="PointGeometry" geometryGeneratorEnabled="0" priority="5" quadOffset="4" maxCurvedCharAngleOut="-25" geometryGenerator="" distMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0" overrunDistanceUnit="MM" placementFlags="10" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" distUnits="MapUnit" repeatDistanceUnits="MM" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" lineAnchorPercent="0.5" offsetType="1" overrunDistance="0"/>
          <rendering fontMinPixelSize="3" upsidedownLabels="0" fontMaxPixelSize="10000" limitNumLabels="0" scaleMin="0" minFeatureSize="0" maxNumLabels="2000" drawLabels="1" obstacleFactor="1" obstacle="1" fontLimitPixelSize="0" obstacleType="1" unplacedVisibility="0" scaleMax="0" labelPerPart="0" scaleVisibility="0" zIndex="0" mergeLines="0" displayAll="0"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="LabelRotation" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="180" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="PositionX" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="0.00125 * cos(pi() * (5/2) - (pi()/180)*to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_2&quot;), '_')[1]))+&quot;longitude&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="PositionY" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="0.00125 * sin(pi() * (5/2) - (pi()/180)*to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_2&quot;), '_')[1]))+&quot;latitude&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option name="anchorPoint" value="pole_of_inaccessibility" type="QString"/>
              <Option name="blendMode" value="0" type="int"/>
              <Option name="ddProperties" type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
              <Option name="drawToAllParts" value="false" type="bool"/>
              <Option name="enabled" value="0" type="QString"/>
              <Option name="labelAnchorPoint" value="point_on_exterior" type="QString"/>
              <Option name="lineSymbol" value="&lt;symbol name=&quot;symbol&quot; alpha=&quot;1&quot; force_rhr=&quot;0&quot; type=&quot;line&quot; clip_to_extent=&quot;1&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer enabled=&quot;1&quot; class=&quot;SimpleLine&quot; locked=&quot;0&quot; pass=&quot;0&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;align_dash_pattern&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;capstyle&quot; value=&quot;square&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash&quot; value=&quot;5;2&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;draw_inside_polygon&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;joinstyle&quot; value=&quot;bevel&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_color&quot; value=&quot;60,60,60,255&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_style&quot; value=&quot;solid&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_width&quot; value=&quot;0.3&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_width_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;ring_filter&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;tweak_dash_pattern_on_corners&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;use_custom_dash&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;width_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_end_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;trim_distance_start&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_start_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_start_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString"/>
              <Option name="minLength" value="0" type="double"/>
              <Option name="minLengthMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="minLengthUnit" value="MM" type="QString"/>
              <Option name="offsetFromAnchor" value="0" type="double"/>
              <Option name="offsetFromAnchorMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromAnchorUnit" value="MM" type="QString"/>
              <Option name="offsetFromLabel" value="0" type="double"/>
              <Option name="offsetFromLabelMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromLabelUnit" value="MM" type="QString"/>
            </Option>
          </callout>
        </settings>
      </rule>
      <rule key="{23dece5a-9b26-4545-b4bb-da079a6cfaa3}">
        <settings calloutType="simple">
          <text-style legendString="Aa" fontItalic="0" capitalization="0" fontKerning="1" textOpacity="1" fontSize="12" fontSizeMapUnitScale="3x:0,0,0,0,0,0" textColor="1,255,5,255" allowHtml="0" isExpression="1" fieldName="string_to_array(file_name(&quot;endereco_imagem_lateral_3&quot;), '_')[1]" useSubstitutions="0" blendMode="0" previewBkgrdColor="255,255,255,255" namedStyle="Regular" fontWordSpacing="0" multilineHeight="1" fontFamily="Open Sans" fontStrikeout="0" fontLetterSpacing="0" fontSizeUnit="Point" textOrientation="horizontal" fontUnderline="0" fontWeight="50">
            <families/>
            <text-buffer bufferColor="0,0,0,255" bufferOpacity="1" bufferSizeUnits="MM" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128" bufferDraw="1" bufferBlendMode="0" bufferSize="1" bufferNoFill="1"/>
            <text-mask maskType="0" maskOpacity="1" maskEnabled="0" maskedSymbolLayers="" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskJoinStyle="128" maskSizeUnits="MM" maskSize="0"/>
            <background shapeOffsetX="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOpacity="1" shapeRadiiUnit="Point" shapeFillColor="255,255,255,255" shapeRotation="0" shapeType="0" shapeSizeY="0" shapeBorderColor="128,128,128,255" shapeRotationType="0" shapeOffsetUnit="Point" shapeSizeUnit="Point" shapeSizeX="0" shapeJoinStyle="64" shapeRadiiX="0" shapeRadiiY="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetY="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeBlendMode="0" shapeSVGFile="" shapeSizeType="0" shapeBorderWidth="0" shapeDraw="0" shapeBorderWidthUnit="Point">
              <symbol name="markerSymbol" alpha="1" force_rhr="0" type="marker" clip_to_extent="1">
                <data_defined_properties>
                  <Option type="Map">
                    <Option name="name" value="" type="QString"/>
                    <Option name="properties"/>
                    <Option name="type" value="collection" type="QString"/>
                  </Option>
                </data_defined_properties>
                <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
                  <Option type="Map">
                    <Option name="angle" value="0" type="QString"/>
                    <Option name="cap_style" value="square" type="QString"/>
                    <Option name="color" value="232,113,141,255" type="QString"/>
                    <Option name="horizontal_anchor_point" value="1" type="QString"/>
                    <Option name="joinstyle" value="bevel" type="QString"/>
                    <Option name="name" value="circle" type="QString"/>
                    <Option name="offset" value="0,0" type="QString"/>
                    <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="offset_unit" value="MM" type="QString"/>
                    <Option name="outline_color" value="35,35,35,255" type="QString"/>
                    <Option name="outline_style" value="solid" type="QString"/>
                    <Option name="outline_width" value="0" type="QString"/>
                    <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="outline_width_unit" value="MM" type="QString"/>
                    <Option name="scale_method" value="diameter" type="QString"/>
                    <Option name="size" value="2" type="QString"/>
                    <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="size_unit" value="MM" type="QString"/>
                    <Option name="vertical_anchor_point" value="1" type="QString"/>
                  </Option>
                  <prop k="angle" v="0"/>
                  <prop k="cap_style" v="square"/>
                  <prop k="color" v="232,113,141,255"/>
                  <prop k="horizontal_anchor_point" v="1"/>
                  <prop k="joinstyle" v="bevel"/>
                  <prop k="name" v="circle"/>
                  <prop k="offset" v="0,0"/>
                  <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="offset_unit" v="MM"/>
                  <prop k="outline_color" v="35,35,35,255"/>
                  <prop k="outline_style" v="solid"/>
                  <prop k="outline_width" v="0"/>
                  <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="outline_width_unit" v="MM"/>
                  <prop k="scale_method" v="diameter"/>
                  <prop k="size" v="2"/>
                  <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="size_unit" v="MM"/>
                  <prop k="vertical_anchor_point" v="1"/>
                  <data_defined_properties>
                    <Option type="Map">
                      <Option name="name" value="" type="QString"/>
                      <Option name="properties"/>
                      <Option name="type" value="collection" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
              <symbol name="fillSymbol" alpha="1" force_rhr="0" type="fill" clip_to_extent="1">
                <data_defined_properties>
                  <Option type="Map">
                    <Option name="name" value="" type="QString"/>
                    <Option name="properties"/>
                    <Option name="type" value="collection" type="QString"/>
                  </Option>
                </data_defined_properties>
                <layer enabled="1" class="SimpleFill" locked="0" pass="0">
                  <Option type="Map">
                    <Option name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="color" value="255,255,255,255" type="QString"/>
                    <Option name="joinstyle" value="bevel" type="QString"/>
                    <Option name="offset" value="0,0" type="QString"/>
                    <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="offset_unit" value="MM" type="QString"/>
                    <Option name="outline_color" value="128,128,128,255" type="QString"/>
                    <Option name="outline_style" value="no" type="QString"/>
                    <Option name="outline_width" value="0" type="QString"/>
                    <Option name="outline_width_unit" value="Point" type="QString"/>
                    <Option name="style" value="solid" type="QString"/>
                  </Option>
                  <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="color" v="255,255,255,255"/>
                  <prop k="joinstyle" v="bevel"/>
                  <prop k="offset" v="0,0"/>
                  <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="offset_unit" v="MM"/>
                  <prop k="outline_color" v="128,128,128,255"/>
                  <prop k="outline_style" v="no"/>
                  <prop k="outline_width" v="0"/>
                  <prop k="outline_width_unit" v="Point"/>
                  <prop k="style" v="solid"/>
                  <data_defined_properties>
                    <Option type="Map">
                      <Option name="name" value="" type="QString"/>
                      <Option name="properties"/>
                      <Option name="type" value="collection" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </background>
            <shadow shadowUnder="0" shadowOffsetDist="1" shadowRadiusAlphaOnly="0" shadowDraw="0" shadowOffsetGlobal="1" shadowRadius="1.5" shadowOffsetUnit="MM" shadowScale="100" shadowOffsetAngle="135" shadowColor="0,0,0,255" shadowOpacity="0.69999999999999996" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusUnit="MM" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowBlendMode="6"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format useMaxLineLengthForAutoWrap="1" addDirectionSymbol="0" rightDirectionSymbol=">" reverseDirectionSymbol="0" decimals="3" placeDirectionSymbol="0" plussign="0" wrapChar="" formatNumbers="0" autoWrapLength="0" multilineAlign="3" leftDirectionSymbol="&lt;"/>
          <placement placement="6" polygonPlacementFlags="2" preserveRotation="1" repeatDistance="0" xOffset="0" dist="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" yOffset="0" centroidWhole="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MM" rotationUnit="AngleDegrees" geometryGeneratorType="PointGeometry" maxCurvedCharAngleIn="25" lineAnchorType="0" lineAnchorClipping="0" rotationAngle="0" centroidInside="0" layerType="PointGeometry" geometryGeneratorEnabled="0" priority="5" quadOffset="4" maxCurvedCharAngleOut="-25" geometryGenerator="" distMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0" overrunDistanceUnit="MM" placementFlags="10" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" distUnits="MapUnit" repeatDistanceUnits="MM" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" lineAnchorPercent="0.5" offsetType="1" overrunDistance="0"/>
          <rendering fontMinPixelSize="3" upsidedownLabels="0" fontMaxPixelSize="10000" limitNumLabels="0" scaleMin="0" minFeatureSize="0" maxNumLabels="2000" drawLabels="1" obstacleFactor="1" obstacle="1" fontLimitPixelSize="0" obstacleType="1" unplacedVisibility="0" scaleMax="0" labelPerPart="0" scaleVisibility="0" zIndex="0" mergeLines="0" displayAll="0"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="LabelRotation" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="180" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="PositionX" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="0.00125 * cos(pi() * (5/2) - (pi()/180)*to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_3&quot;), '_')[1]))+&quot;longitude&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="PositionY" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="0.00125 * sin(pi() * (5/2) - (pi()/180)*to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_3&quot;), '_')[1]))+&quot;latitude&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option name="anchorPoint" value="pole_of_inaccessibility" type="QString"/>
              <Option name="blendMode" value="0" type="int"/>
              <Option name="ddProperties" type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
              <Option name="drawToAllParts" value="false" type="bool"/>
              <Option name="enabled" value="0" type="QString"/>
              <Option name="labelAnchorPoint" value="point_on_exterior" type="QString"/>
              <Option name="lineSymbol" value="&lt;symbol name=&quot;symbol&quot; alpha=&quot;1&quot; force_rhr=&quot;0&quot; type=&quot;line&quot; clip_to_extent=&quot;1&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer enabled=&quot;1&quot; class=&quot;SimpleLine&quot; locked=&quot;0&quot; pass=&quot;0&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;align_dash_pattern&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;capstyle&quot; value=&quot;square&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash&quot; value=&quot;5;2&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;draw_inside_polygon&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;joinstyle&quot; value=&quot;bevel&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_color&quot; value=&quot;60,60,60,255&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_style&quot; value=&quot;solid&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_width&quot; value=&quot;0.3&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_width_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;ring_filter&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;tweak_dash_pattern_on_corners&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;use_custom_dash&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;width_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_end_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;trim_distance_start&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_start_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_start_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString"/>
              <Option name="minLength" value="0" type="double"/>
              <Option name="minLengthMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="minLengthUnit" value="MM" type="QString"/>
              <Option name="offsetFromAnchor" value="0" type="double"/>
              <Option name="offsetFromAnchorMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromAnchorUnit" value="MM" type="QString"/>
              <Option name="offsetFromLabel" value="0" type="double"/>
              <Option name="offsetFromLabelMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromLabelUnit" value="MM" type="QString"/>
            </Option>
          </callout>
        </settings>
      </rule>
      <rule key="{8face2e6-8861-49cd-a36d-abf0ea3fe9ac}">
        <settings calloutType="simple">
          <text-style legendString="Aa" fontItalic="0" capitalization="0" fontKerning="1" textOpacity="1" fontSize="12" fontSizeMapUnitScale="3x:0,0,0,0,0,0" textColor="1,255,9,255" allowHtml="0" isExpression="1" fieldName="string_to_array(file_name(&quot;endereco_imagem_lateral_4&quot;),'_')[1]" useSubstitutions="0" blendMode="0" previewBkgrdColor="255,255,255,255" namedStyle="Regular" fontWordSpacing="0" multilineHeight="1" fontFamily="Open Sans" fontStrikeout="0" fontLetterSpacing="0" fontSizeUnit="Point" textOrientation="horizontal" fontUnderline="0" fontWeight="50">
            <families/>
            <text-buffer bufferColor="0,0,0,255" bufferOpacity="1" bufferSizeUnits="MM" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128" bufferDraw="1" bufferBlendMode="0" bufferSize="1" bufferNoFill="1"/>
            <text-mask maskType="0" maskOpacity="1" maskEnabled="0" maskedSymbolLayers="" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskJoinStyle="128" maskSizeUnits="MM" maskSize="0"/>
            <background shapeOffsetX="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOpacity="1" shapeRadiiUnit="Point" shapeFillColor="255,255,255,255" shapeRotation="0" shapeType="0" shapeSizeY="0" shapeBorderColor="128,128,128,255" shapeRotationType="0" shapeOffsetUnit="Point" shapeSizeUnit="Point" shapeSizeX="0" shapeJoinStyle="64" shapeRadiiX="0" shapeRadiiY="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetY="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeBlendMode="0" shapeSVGFile="" shapeSizeType="0" shapeBorderWidth="0" shapeDraw="0" shapeBorderWidthUnit="Point">
              <symbol name="markerSymbol" alpha="1" force_rhr="0" type="marker" clip_to_extent="1">
                <data_defined_properties>
                  <Option type="Map">
                    <Option name="name" value="" type="QString"/>
                    <Option name="properties"/>
                    <Option name="type" value="collection" type="QString"/>
                  </Option>
                </data_defined_properties>
                <layer enabled="1" class="SimpleMarker" locked="0" pass="0">
                  <Option type="Map">
                    <Option name="angle" value="0" type="QString"/>
                    <Option name="cap_style" value="square" type="QString"/>
                    <Option name="color" value="232,113,141,255" type="QString"/>
                    <Option name="horizontal_anchor_point" value="1" type="QString"/>
                    <Option name="joinstyle" value="bevel" type="QString"/>
                    <Option name="name" value="circle" type="QString"/>
                    <Option name="offset" value="0,0" type="QString"/>
                    <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="offset_unit" value="MM" type="QString"/>
                    <Option name="outline_color" value="35,35,35,255" type="QString"/>
                    <Option name="outline_style" value="solid" type="QString"/>
                    <Option name="outline_width" value="0" type="QString"/>
                    <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="outline_width_unit" value="MM" type="QString"/>
                    <Option name="scale_method" value="diameter" type="QString"/>
                    <Option name="size" value="2" type="QString"/>
                    <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="size_unit" value="MM" type="QString"/>
                    <Option name="vertical_anchor_point" value="1" type="QString"/>
                  </Option>
                  <prop k="angle" v="0"/>
                  <prop k="cap_style" v="square"/>
                  <prop k="color" v="232,113,141,255"/>
                  <prop k="horizontal_anchor_point" v="1"/>
                  <prop k="joinstyle" v="bevel"/>
                  <prop k="name" v="circle"/>
                  <prop k="offset" v="0,0"/>
                  <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="offset_unit" v="MM"/>
                  <prop k="outline_color" v="35,35,35,255"/>
                  <prop k="outline_style" v="solid"/>
                  <prop k="outline_width" v="0"/>
                  <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="outline_width_unit" v="MM"/>
                  <prop k="scale_method" v="diameter"/>
                  <prop k="size" v="2"/>
                  <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="size_unit" v="MM"/>
                  <prop k="vertical_anchor_point" v="1"/>
                  <data_defined_properties>
                    <Option type="Map">
                      <Option name="name" value="" type="QString"/>
                      <Option name="properties"/>
                      <Option name="type" value="collection" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
              <symbol name="fillSymbol" alpha="1" force_rhr="0" type="fill" clip_to_extent="1">
                <data_defined_properties>
                  <Option type="Map">
                    <Option name="name" value="" type="QString"/>
                    <Option name="properties"/>
                    <Option name="type" value="collection" type="QString"/>
                  </Option>
                </data_defined_properties>
                <layer enabled="1" class="SimpleFill" locked="0" pass="0">
                  <Option type="Map">
                    <Option name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="color" value="255,255,255,255" type="QString"/>
                    <Option name="joinstyle" value="bevel" type="QString"/>
                    <Option name="offset" value="0,0" type="QString"/>
                    <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
                    <Option name="offset_unit" value="MM" type="QString"/>
                    <Option name="outline_color" value="128,128,128,255" type="QString"/>
                    <Option name="outline_style" value="no" type="QString"/>
                    <Option name="outline_width" value="0" type="QString"/>
                    <Option name="outline_width_unit" value="Point" type="QString"/>
                    <Option name="style" value="solid" type="QString"/>
                  </Option>
                  <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="color" v="255,255,255,255"/>
                  <prop k="joinstyle" v="bevel"/>
                  <prop k="offset" v="0,0"/>
                  <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
                  <prop k="offset_unit" v="MM"/>
                  <prop k="outline_color" v="128,128,128,255"/>
                  <prop k="outline_style" v="no"/>
                  <prop k="outline_width" v="0"/>
                  <prop k="outline_width_unit" v="Point"/>
                  <prop k="style" v="solid"/>
                  <data_defined_properties>
                    <Option type="Map">
                      <Option name="name" value="" type="QString"/>
                      <Option name="properties"/>
                      <Option name="type" value="collection" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </background>
            <shadow shadowUnder="0" shadowOffsetDist="1" shadowRadiusAlphaOnly="0" shadowDraw="0" shadowOffsetGlobal="1" shadowRadius="1.5" shadowOffsetUnit="MM" shadowScale="100" shadowOffsetAngle="135" shadowColor="0,0,0,255" shadowOpacity="0.69999999999999996" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusUnit="MM" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowBlendMode="6"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format useMaxLineLengthForAutoWrap="1" addDirectionSymbol="0" rightDirectionSymbol=">" reverseDirectionSymbol="0" decimals="3" placeDirectionSymbol="0" plussign="0" wrapChar="" formatNumbers="0" autoWrapLength="0" multilineAlign="3" leftDirectionSymbol="&lt;"/>
          <placement placement="6" polygonPlacementFlags="2" preserveRotation="1" repeatDistance="0" xOffset="0" dist="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" yOffset="0" centroidWhole="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MM" rotationUnit="AngleDegrees" geometryGeneratorType="PointGeometry" maxCurvedCharAngleIn="25" lineAnchorType="0" lineAnchorClipping="0" rotationAngle="0" centroidInside="0" layerType="PointGeometry" geometryGeneratorEnabled="0" priority="5" quadOffset="4" maxCurvedCharAngleOut="-25" geometryGenerator="" distMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0" overrunDistanceUnit="MM" placementFlags="10" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" distUnits="MapUnit" repeatDistanceUnits="MM" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" lineAnchorPercent="0.5" offsetType="1" overrunDistance="0"/>
          <rendering fontMinPixelSize="3" upsidedownLabels="0" fontMaxPixelSize="10000" limitNumLabels="0" scaleMin="0" minFeatureSize="0" maxNumLabels="2000" drawLabels="1" obstacleFactor="1" obstacle="1" fontLimitPixelSize="0" obstacleType="1" unplacedVisibility="0" scaleMax="0" labelPerPart="0" scaleVisibility="0" zIndex="0" mergeLines="0" displayAll="0"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="LabelRotation" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="180" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="PositionX" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="0.00125 * cos(pi() * (5/2) - (pi()/180)*to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_4&quot;), '_')[1]))+&quot;longitude&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
                <Option name="PositionY" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="0.00125 * sin(pi() * (5/2) - (pi()/180)*to_real(string_to_array(file_name(&quot;endereco_imagem_lateral_4&quot;), '_')[1]))+&quot;latitude&quot;" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option name="anchorPoint" value="pole_of_inaccessibility" type="QString"/>
              <Option name="blendMode" value="0" type="int"/>
              <Option name="ddProperties" type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
              <Option name="drawToAllParts" value="false" type="bool"/>
              <Option name="enabled" value="0" type="QString"/>
              <Option name="labelAnchorPoint" value="point_on_exterior" type="QString"/>
              <Option name="lineSymbol" value="&lt;symbol name=&quot;symbol&quot; alpha=&quot;1&quot; force_rhr=&quot;0&quot; type=&quot;line&quot; clip_to_extent=&quot;1&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer enabled=&quot;1&quot; class=&quot;SimpleLine&quot; locked=&quot;0&quot; pass=&quot;0&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;align_dash_pattern&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;capstyle&quot; value=&quot;square&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash&quot; value=&quot;5;2&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;customdash_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;dash_pattern_offset_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;draw_inside_polygon&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;joinstyle&quot; value=&quot;bevel&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_color&quot; value=&quot;60,60,60,255&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_style&quot; value=&quot;solid&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_width&quot; value=&quot;0.3&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;line_width_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;offset_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;ring_filter&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_end_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;trim_distance_start_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;tweak_dash_pattern_on_corners&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;use_custom_dash&quot; value=&quot;0&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;width_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_end_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;trim_distance_start&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_start_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_start_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString"/>
              <Option name="minLength" value="0" type="double"/>
              <Option name="minLengthMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="minLengthUnit" value="MM" type="QString"/>
              <Option name="offsetFromAnchor" value="0" type="double"/>
              <Option name="offsetFromAnchorMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromAnchorUnit" value="MM" type="QString"/>
              <Option name="offsetFromLabel" value="0" type="double"/>
              <Option name="offsetFromLabelMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromLabelUnit" value="MM" type="QString"/>
            </Option>
          </callout>
        </settings>
      </rule>
    </rules>
  </labeling>
  <customproperties>
    <Option type="Map">
      <Option name="dualview/previewExpressions" type="List">
        <Option value="&quot;cod_ponto&quot;" type="QString"/>
      </Option>
      <Option name="embeddedWidgets/count" value="0" type="int"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory barWidth="5" rotationOffset="270" backgroundAlpha="255" lineSizeScale="3x:0,0,0,0,0,0" showAxis="1" spacing="5" lineSizeType="MM" width="15" labelPlacementMethod="XHeight" backgroundColor="#ffffff" sizeType="MM" scaleBasedVisibility="0" scaleDependency="Area" penWidth="0" sizeScale="3x:0,0,0,0,0,0" minimumSize="0" penAlpha="255" direction="0" height="15" maxScaleDenominator="1e+08" opacity="1" enabled="0" minScaleDenominator="0" diagramOrientation="Up" spacingUnitScale="3x:0,0,0,0,0,0" spacingUnit="MM" penColor="#000000">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute field="" color="#000000" label=""/>
      <axisSymbol>
        <symbol name="" alpha="1" force_rhr="0" type="line" clip_to_extent="1">
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
          <layer enabled="1" class="SimpleLine" locked="0" pass="0">
            <Option type="Map">
              <Option name="align_dash_pattern" value="0" type="QString"/>
              <Option name="capstyle" value="square" type="QString"/>
              <Option name="customdash" value="5;2" type="QString"/>
              <Option name="customdash_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="customdash_unit" value="MM" type="QString"/>
              <Option name="dash_pattern_offset" value="0" type="QString"/>
              <Option name="dash_pattern_offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="dash_pattern_offset_unit" value="MM" type="QString"/>
              <Option name="draw_inside_polygon" value="0" type="QString"/>
              <Option name="joinstyle" value="bevel" type="QString"/>
              <Option name="line_color" value="35,35,35,255" type="QString"/>
              <Option name="line_style" value="solid" type="QString"/>
              <Option name="line_width" value="0.26" type="QString"/>
              <Option name="line_width_unit" value="MM" type="QString"/>
              <Option name="offset" value="0" type="QString"/>
              <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offset_unit" value="MM" type="QString"/>
              <Option name="ring_filter" value="0" type="QString"/>
              <Option name="trim_distance_end" value="0" type="QString"/>
              <Option name="trim_distance_end_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="trim_distance_end_unit" value="MM" type="QString"/>
              <Option name="trim_distance_start" value="0" type="QString"/>
              <Option name="trim_distance_start_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="trim_distance_start_unit" value="MM" type="QString"/>
              <Option name="tweak_dash_pattern_on_corners" value="0" type="QString"/>
              <Option name="use_custom_dash" value="0" type="QString"/>
              <Option name="width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString"/>
            </Option>
            <prop k="align_dash_pattern" v="0"/>
            <prop k="capstyle" v="square"/>
            <prop k="customdash" v="5;2"/>
            <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="customdash_unit" v="MM"/>
            <prop k="dash_pattern_offset" v="0"/>
            <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="dash_pattern_offset_unit" v="MM"/>
            <prop k="draw_inside_polygon" v="0"/>
            <prop k="joinstyle" v="bevel"/>
            <prop k="line_color" v="35,35,35,255"/>
            <prop k="line_style" v="solid"/>
            <prop k="line_width" v="0.26"/>
            <prop k="line_width_unit" v="MM"/>
            <prop k="offset" v="0"/>
            <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="offset_unit" v="MM"/>
            <prop k="ring_filter" v="0"/>
            <prop k="trim_distance_end" v="0"/>
            <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="trim_distance_end_unit" v="MM"/>
            <prop k="trim_distance_start" v="0"/>
            <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="trim_distance_start_unit" v="MM"/>
            <prop k="tweak_dash_pattern_on_corners" v="0"/>
            <prop k="use_custom_dash" v="0"/>
            <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings obstacle="0" priority="0" zIndex="0" dist="0" placement="0" showAll="1" linePlacementFlags="18">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <legend showLabelLegend="0" type="default-vector"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field name="id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="cod_ponto" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="data_rastreio" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="tipo_ref" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" value="9999" type="QString"/>
              <Option name="Altimétrico" value="1" type="QString"/>
              <Option name="Gravimétrico" value="4" type="QString"/>
              <Option name="Planialtimétrico" value="3" type="QString"/>
              <Option name="Planimétrico" value="2" type="QString"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="latitude" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="longitude" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="norte" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="leste" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="altitude_ortometrica" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="altitude_geometrica" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="sistema_geodesico" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" value="9999" type="QString"/>
              <Option name="Astro Chuá" value="5" type="QString"/>
              <Option name="Córrego Alegre" value="4" type="QString"/>
              <Option name="Outra referência" value="99" type="QString"/>
              <Option name="SAD-69" value="1" type="QString"/>
              <Option name="SAD-69 (96)" value="6" type="QString"/>
              <Option name="SIRGAS2000" value="2" type="QString"/>
              <Option name="WGS-84" value="3" type="QString"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="outra_ref_plan" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="referencial_altim" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" value="9999" type="QString"/>
              <Option name="Imbituba" value="2" type="QString"/>
              <Option name="Outra referência" value="99" type="QString"/>
              <Option name="Santana" value="3" type="QString"/>
              <Option name="Torres" value="1" type="QString"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="outro_ref_alt" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="fuso" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="meridiano_central" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="tipo_situacao" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" value="9999" type="QString"/>
              <Option name="Aguardando revisão" value="2" type="QString"/>
              <Option name="Aprovado" value="3" type="QString"/>
              <Option name="Não medido" value="1" type="QString"/>
              <Option name="Reprovado" value="4" type="QString"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="reserva" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="lote" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="latitude_planejada" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="longitude_planejada" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="medidor" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="inicio_rastreio" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="fim_rastreio" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="classificacao_ponto" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" value="9999" type="QString"/>
              <Option name="Abaixo de vegetação" value="7" type="QString"/>
              <Option name="Canto de edificação" value="1" type="QString"/>
              <Option name="Cerca ou muro" value="3" type="QString"/>
              <Option name="Desconhecido" value="0" type="QString"/>
              <Option name="Elemento identificável no solo" value="4" type="QString"/>
              <Option name="Elemento não identificável no solo" value="5" type="QString"/>
              <Option name="Entroncamento de estrada" value="2" type="QString"/>
              <Option name="Topo de vegetação" value="6" type="QString"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="observacao" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="metodo_posicionamento" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" value="9999" type="QString"/>
              <Option name="Absoluto" value="6" type="QString"/>
              <Option name="Posicionamento por ponto preciso (PPP)" value="1" type="QString"/>
              <Option name="Real Time Kinematic (RTK)" value="2" type="QString"/>
              <Option name="Relativo Cinemático" value="5" type="QString"/>
              <Option name="Relativo Estático" value="4" type="QString"/>
              <Option name="Semi-cinemático" value="3" type="QString"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="ponto_base" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="materializado" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="altura_antena" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="tipo_medicao_altura" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" value="9999" type="QString"/>
              <Option name="Altura inclinada" value="2" type="QString"/>
              <Option name="Base de montagem" value="1" type="QString"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="referencia_medicao_altura" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" value="9999" type="QString"/>
              <Option name="Nível do objeto" value="2" type="QString"/>
              <Option name="Nível do solo" value="1" type="QString"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="altura_objeto" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="mascara_elevacao" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="taxa_gravacao" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="modelo_gps" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="modelo_antena" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="numero_serie_gps" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="numero_serie_antena" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="modelo_geoidal" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="precisao_horizontal_esperada" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="precisao_vertical_esperada" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="freq_processada" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="data_processamento" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="orbita" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" value="9999" type="QString"/>
              <Option name="Final" value="4" type="QString"/>
              <Option name="Não aplicável" value="97" type="QString"/>
              <Option name="Rápida" value="3" type="QString"/>
              <Option name="Ultra Rápida (observada)" value="2" type="QString"/>
              <Option name="Ultra Rápida (predita)" value="1" type="QString"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orgao_executante" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="projeto" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="engenheiro_responsavel" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="crea_engenheiro_responsavel" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="cpf_engenheiro_responsavel" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="geometria_aproximada" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="tipo_pto_ref_geod_topo" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" value="9999" type="QString"/>
              <Option name="Desconhecido" value="0" type="QString"/>
              <Option name="Estação de poligonal - EP" value="4" type="QString"/>
              <Option name="Estação gravimétrica - EG" value="3" type="QString"/>
              <Option name="Outros" value="99" type="QString"/>
              <Option name="Ponto astronômico - PA" value="5" type="QString"/>
              <Option name="Ponto barométrico - B" value="6" type="QString"/>
              <Option name="Ponto de satélite - SAT" value="8" type="QString"/>
              <Option name="Ponto trigonométrico - RV" value="7" type="QString"/>
              <Option name="Referência de nível - RN" value="2" type="QString"/>
              <Option name="Vértice de triangulação - VT" value="1" type="QString"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipo_marco_limite" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" value="9999" type="QString"/>
              <Option name="Estadual" value="23" type="QString"/>
              <Option name="Internacional de referência" value="25" type="QString"/>
              <Option name="Internacional principal" value="26" type="QString"/>
              <Option name="Internacional secundário" value="24" type="QString"/>
              <Option name="Municipal" value="3" type="QString"/>
              <Option name="Não aplicável" value="97" type="QString"/>
              <Option name="Outros" value="99" type="QString"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="rede_referencia" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" value="9999" type="QString"/>
              <Option name="Desconhecida" value="0" type="QString"/>
              <Option name="Estadual" value="2" type="QString"/>
              <Option name="Municipal" value="3" type="QString"/>
              <Option name="Nacional" value="14" type="QString"/>
              <Option name="Não aplicável" value="97" type="QString"/>
              <Option name="Privada" value="15" type="QString"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="referencial_grav" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" value="9999" type="QString"/>
              <Option name="Absoluto" value="3" type="QString"/>
              <Option name="Desconhecido" value="0" type="QString"/>
              <Option name="IGSN71" value="2" type="QString"/>
              <Option name="Local" value="4" type="QString"/>
              <Option name="Não aplicável" value="97" type="QString"/>
              <Option name="Potsdam 1930" value="1" type="QString"/>
              <Option name="RGFB" value="5" type="QString"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="situacao_marco" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" value="9999" type="QString"/>
              <Option name="Bom" value="1" type="QString"/>
              <Option name="Desconhecida" value="0" type="QString"/>
              <Option name="Destruído" value="2" type="QString"/>
              <Option name="Destruído sem chapa" value="3" type="QString"/>
              <Option name="Destruí­do com chapa danificada" value="4" type="QString"/>
              <Option name="Não construí­do" value="7" type="QString"/>
              <Option name="Não encontrado" value="5" type="QString"/>
              <Option name="Não visitado" value="6" type="QString"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="data_visita" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="valor_gravidade" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="possui_monografia" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="numero_fotos" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="possui_croqui" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="possui_arquivo_rastreio" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="endereco_imagem_lateral_1" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="endereco_imagem_lateral_2" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="endereco_imagem_lateral_3" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="endereco_imagem_lateral_4" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="endereco_imagem_aerea" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" index="0" field="id"/>
    <alias name="" index="1" field="cod_ponto"/>
    <alias name="" index="2" field="data_rastreio"/>
    <alias name="" index="3" field="tipo_ref"/>
    <alias name="" index="4" field="latitude"/>
    <alias name="" index="5" field="longitude"/>
    <alias name="" index="6" field="norte"/>
    <alias name="" index="7" field="leste"/>
    <alias name="" index="8" field="altitude_ortometrica"/>
    <alias name="" index="9" field="altitude_geometrica"/>
    <alias name="" index="10" field="sistema_geodesico"/>
    <alias name="" index="11" field="outra_ref_plan"/>
    <alias name="" index="12" field="referencial_altim"/>
    <alias name="" index="13" field="outro_ref_alt"/>
    <alias name="" index="14" field="fuso"/>
    <alias name="" index="15" field="meridiano_central"/>
    <alias name="" index="16" field="tipo_situacao"/>
    <alias name="" index="17" field="reserva"/>
    <alias name="" index="18" field="lote"/>
    <alias name="" index="19" field="latitude_planejada"/>
    <alias name="" index="20" field="longitude_planejada"/>
    <alias name="" index="21" field="medidor"/>
    <alias name="" index="22" field="inicio_rastreio"/>
    <alias name="" index="23" field="fim_rastreio"/>
    <alias name="" index="24" field="classificacao_ponto"/>
    <alias name="" index="25" field="observacao"/>
    <alias name="" index="26" field="metodo_posicionamento"/>
    <alias name="" index="27" field="ponto_base"/>
    <alias name="" index="28" field="materializado"/>
    <alias name="" index="29" field="altura_antena"/>
    <alias name="" index="30" field="tipo_medicao_altura"/>
    <alias name="" index="31" field="referencia_medicao_altura"/>
    <alias name="" index="32" field="altura_objeto"/>
    <alias name="" index="33" field="mascara_elevacao"/>
    <alias name="" index="34" field="taxa_gravacao"/>
    <alias name="" index="35" field="modelo_gps"/>
    <alias name="" index="36" field="modelo_antena"/>
    <alias name="" index="37" field="numero_serie_gps"/>
    <alias name="" index="38" field="numero_serie_antena"/>
    <alias name="" index="39" field="modelo_geoidal"/>
    <alias name="" index="40" field="precisao_horizontal_esperada"/>
    <alias name="" index="41" field="precisao_vertical_esperada"/>
    <alias name="" index="42" field="freq_processada"/>
    <alias name="" index="43" field="data_processamento"/>
    <alias name="" index="44" field="orbita"/>
    <alias name="" index="45" field="orgao_executante"/>
    <alias name="" index="46" field="projeto"/>
    <alias name="" index="47" field="engenheiro_responsavel"/>
    <alias name="" index="48" field="crea_engenheiro_responsavel"/>
    <alias name="" index="49" field="cpf_engenheiro_responsavel"/>
    <alias name="" index="50" field="geometria_aproximada"/>
    <alias name="" index="51" field="tipo_pto_ref_geod_topo"/>
    <alias name="" index="52" field="tipo_marco_limite"/>
    <alias name="" index="53" field="rede_referencia"/>
    <alias name="" index="54" field="referencial_grav"/>
    <alias name="" index="55" field="situacao_marco"/>
    <alias name="" index="56" field="data_visita"/>
    <alias name="" index="57" field="valor_gravidade"/>
    <alias name="" index="58" field="possui_monografia"/>
    <alias name="" index="59" field="numero_fotos"/>
    <alias name="" index="60" field="possui_croqui"/>
    <alias name="" index="61" field="possui_arquivo_rastreio"/>
    <alias name="" index="62" field="endereco_imagem_lateral_1"/>
    <alias name="" index="63" field="endereco_imagem_lateral_2"/>
    <alias name="" index="64" field="endereco_imagem_lateral_3"/>
    <alias name="" index="65" field="endereco_imagem_lateral_4"/>
    <alias name="" index="66" field="endereco_imagem_aerea"/>
  </aliases>
  <defaults>
    <default applyOnUpdate="0" expression="" field="id"/>
    <default applyOnUpdate="0" expression="" field="cod_ponto"/>
    <default applyOnUpdate="0" expression="" field="data_rastreio"/>
    <default applyOnUpdate="0" expression="" field="tipo_ref"/>
    <default applyOnUpdate="0" expression="" field="latitude"/>
    <default applyOnUpdate="0" expression="" field="longitude"/>
    <default applyOnUpdate="0" expression="" field="norte"/>
    <default applyOnUpdate="0" expression="" field="leste"/>
    <default applyOnUpdate="0" expression="" field="altitude_ortometrica"/>
    <default applyOnUpdate="0" expression="" field="altitude_geometrica"/>
    <default applyOnUpdate="0" expression="" field="sistema_geodesico"/>
    <default applyOnUpdate="0" expression="" field="outra_ref_plan"/>
    <default applyOnUpdate="0" expression="" field="referencial_altim"/>
    <default applyOnUpdate="0" expression="" field="outro_ref_alt"/>
    <default applyOnUpdate="0" expression="" field="fuso"/>
    <default applyOnUpdate="0" expression="" field="meridiano_central"/>
    <default applyOnUpdate="0" expression="" field="tipo_situacao"/>
    <default applyOnUpdate="0" expression="" field="reserva"/>
    <default applyOnUpdate="0" expression="" field="lote"/>
    <default applyOnUpdate="0" expression="" field="latitude_planejada"/>
    <default applyOnUpdate="0" expression="" field="longitude_planejada"/>
    <default applyOnUpdate="0" expression="" field="medidor"/>
    <default applyOnUpdate="0" expression="" field="inicio_rastreio"/>
    <default applyOnUpdate="0" expression="" field="fim_rastreio"/>
    <default applyOnUpdate="0" expression="" field="classificacao_ponto"/>
    <default applyOnUpdate="0" expression="" field="observacao"/>
    <default applyOnUpdate="0" expression="" field="metodo_posicionamento"/>
    <default applyOnUpdate="0" expression="" field="ponto_base"/>
    <default applyOnUpdate="0" expression="" field="materializado"/>
    <default applyOnUpdate="0" expression="" field="altura_antena"/>
    <default applyOnUpdate="0" expression="" field="tipo_medicao_altura"/>
    <default applyOnUpdate="0" expression="" field="referencia_medicao_altura"/>
    <default applyOnUpdate="0" expression="" field="altura_objeto"/>
    <default applyOnUpdate="0" expression="" field="mascara_elevacao"/>
    <default applyOnUpdate="0" expression="" field="taxa_gravacao"/>
    <default applyOnUpdate="0" expression="" field="modelo_gps"/>
    <default applyOnUpdate="0" expression="" field="modelo_antena"/>
    <default applyOnUpdate="0" expression="" field="numero_serie_gps"/>
    <default applyOnUpdate="0" expression="" field="numero_serie_antena"/>
    <default applyOnUpdate="0" expression="" field="modelo_geoidal"/>
    <default applyOnUpdate="0" expression="" field="precisao_horizontal_esperada"/>
    <default applyOnUpdate="0" expression="" field="precisao_vertical_esperada"/>
    <default applyOnUpdate="0" expression="" field="freq_processada"/>
    <default applyOnUpdate="0" expression="" field="data_processamento"/>
    <default applyOnUpdate="0" expression="" field="orbita"/>
    <default applyOnUpdate="0" expression="" field="orgao_executante"/>
    <default applyOnUpdate="0" expression="" field="projeto"/>
    <default applyOnUpdate="0" expression="" field="engenheiro_responsavel"/>
    <default applyOnUpdate="0" expression="" field="crea_engenheiro_responsavel"/>
    <default applyOnUpdate="0" expression="" field="cpf_engenheiro_responsavel"/>
    <default applyOnUpdate="0" expression="" field="geometria_aproximada"/>
    <default applyOnUpdate="0" expression="" field="tipo_pto_ref_geod_topo"/>
    <default applyOnUpdate="0" expression="" field="tipo_marco_limite"/>
    <default applyOnUpdate="0" expression="" field="rede_referencia"/>
    <default applyOnUpdate="0" expression="" field="referencial_grav"/>
    <default applyOnUpdate="0" expression="" field="situacao_marco"/>
    <default applyOnUpdate="0" expression="" field="data_visita"/>
    <default applyOnUpdate="0" expression="" field="valor_gravidade"/>
    <default applyOnUpdate="0" expression="" field="possui_monografia"/>
    <default applyOnUpdate="0" expression="" field="numero_fotos"/>
    <default applyOnUpdate="0" expression="" field="possui_croqui"/>
    <default applyOnUpdate="0" expression="" field="possui_arquivo_rastreio"/>
    <default applyOnUpdate="0" expression="" field="endereco_imagem_lateral_1"/>
    <default applyOnUpdate="0" expression="" field="endereco_imagem_lateral_2"/>
    <default applyOnUpdate="0" expression="" field="endereco_imagem_lateral_3"/>
    <default applyOnUpdate="0" expression="" field="endereco_imagem_lateral_4"/>
    <default applyOnUpdate="0" expression="" field="endereco_imagem_aerea"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" exp_strength="0" field="id" unique_strength="1" constraints="3"/>
    <constraint notnull_strength="1" exp_strength="0" field="cod_ponto" unique_strength="1" constraints="3"/>
    <constraint notnull_strength="1" exp_strength="0" field="data_rastreio" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="1" exp_strength="0" field="tipo_ref" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" exp_strength="0" field="latitude" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="longitude" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="norte" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="leste" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="altitude_ortometrica" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="altitude_geometrica" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="1" exp_strength="0" field="sistema_geodesico" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" exp_strength="0" field="outra_ref_plan" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="1" exp_strength="0" field="referencial_altim" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" exp_strength="0" field="outro_ref_alt" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="fuso" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="meridiano_central" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="1" exp_strength="0" field="tipo_situacao" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="1" exp_strength="0" field="reserva" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" exp_strength="0" field="lote" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="latitude_planejada" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="longitude_planejada" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="medidor" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="inicio_rastreio" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="fim_rastreio" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="1" exp_strength="0" field="classificacao_ponto" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" exp_strength="0" field="observacao" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="1" exp_strength="0" field="metodo_posicionamento" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" exp_strength="0" field="ponto_base" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="1" exp_strength="0" field="materializado" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" exp_strength="0" field="altura_antena" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="1" exp_strength="0" field="tipo_medicao_altura" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="1" exp_strength="0" field="referencia_medicao_altura" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" exp_strength="0" field="altura_objeto" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="mascara_elevacao" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="taxa_gravacao" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="modelo_gps" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="modelo_antena" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="numero_serie_gps" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="numero_serie_antena" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="modelo_geoidal" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="precisao_horizontal_esperada" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="precisao_vertical_esperada" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="freq_processada" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="data_processamento" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="1" exp_strength="0" field="orbita" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" exp_strength="0" field="orgao_executante" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="projeto" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="engenheiro_responsavel" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="crea_engenheiro_responsavel" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="cpf_engenheiro_responsavel" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="1" exp_strength="0" field="geometria_aproximada" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="1" exp_strength="0" field="tipo_pto_ref_geod_topo" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="1" exp_strength="0" field="tipo_marco_limite" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="1" exp_strength="0" field="rede_referencia" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="1" exp_strength="0" field="referencial_grav" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="1" exp_strength="0" field="situacao_marco" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" exp_strength="0" field="data_visita" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="valor_gravidade" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="1" exp_strength="0" field="possui_monografia" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" exp_strength="0" field="numero_fotos" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="1" exp_strength="0" field="possui_croqui" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="1" exp_strength="0" field="possui_arquivo_rastreio" unique_strength="0" constraints="1"/>
    <constraint notnull_strength="0" exp_strength="0" field="endereco_imagem_lateral_1" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="endereco_imagem_lateral_2" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="endereco_imagem_lateral_3" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="endereco_imagem_lateral_4" unique_strength="0" constraints="0"/>
    <constraint notnull_strength="0" exp_strength="0" field="endereco_imagem_aerea" unique_strength="0" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="id"/>
    <constraint desc="" exp="" field="cod_ponto"/>
    <constraint desc="" exp="" field="data_rastreio"/>
    <constraint desc="" exp="" field="tipo_ref"/>
    <constraint desc="" exp="" field="latitude"/>
    <constraint desc="" exp="" field="longitude"/>
    <constraint desc="" exp="" field="norte"/>
    <constraint desc="" exp="" field="leste"/>
    <constraint desc="" exp="" field="altitude_ortometrica"/>
    <constraint desc="" exp="" field="altitude_geometrica"/>
    <constraint desc="" exp="" field="sistema_geodesico"/>
    <constraint desc="" exp="" field="outra_ref_plan"/>
    <constraint desc="" exp="" field="referencial_altim"/>
    <constraint desc="" exp="" field="outro_ref_alt"/>
    <constraint desc="" exp="" field="fuso"/>
    <constraint desc="" exp="" field="meridiano_central"/>
    <constraint desc="" exp="" field="tipo_situacao"/>
    <constraint desc="" exp="" field="reserva"/>
    <constraint desc="" exp="" field="lote"/>
    <constraint desc="" exp="" field="latitude_planejada"/>
    <constraint desc="" exp="" field="longitude_planejada"/>
    <constraint desc="" exp="" field="medidor"/>
    <constraint desc="" exp="" field="inicio_rastreio"/>
    <constraint desc="" exp="" field="fim_rastreio"/>
    <constraint desc="" exp="" field="classificacao_ponto"/>
    <constraint desc="" exp="" field="observacao"/>
    <constraint desc="" exp="" field="metodo_posicionamento"/>
    <constraint desc="" exp="" field="ponto_base"/>
    <constraint desc="" exp="" field="materializado"/>
    <constraint desc="" exp="" field="altura_antena"/>
    <constraint desc="" exp="" field="tipo_medicao_altura"/>
    <constraint desc="" exp="" field="referencia_medicao_altura"/>
    <constraint desc="" exp="" field="altura_objeto"/>
    <constraint desc="" exp="" field="mascara_elevacao"/>
    <constraint desc="" exp="" field="taxa_gravacao"/>
    <constraint desc="" exp="" field="modelo_gps"/>
    <constraint desc="" exp="" field="modelo_antena"/>
    <constraint desc="" exp="" field="numero_serie_gps"/>
    <constraint desc="" exp="" field="numero_serie_antena"/>
    <constraint desc="" exp="" field="modelo_geoidal"/>
    <constraint desc="" exp="" field="precisao_horizontal_esperada"/>
    <constraint desc="" exp="" field="precisao_vertical_esperada"/>
    <constraint desc="" exp="" field="freq_processada"/>
    <constraint desc="" exp="" field="data_processamento"/>
    <constraint desc="" exp="" field="orbita"/>
    <constraint desc="" exp="" field="orgao_executante"/>
    <constraint desc="" exp="" field="projeto"/>
    <constraint desc="" exp="" field="engenheiro_responsavel"/>
    <constraint desc="" exp="" field="crea_engenheiro_responsavel"/>
    <constraint desc="" exp="" field="cpf_engenheiro_responsavel"/>
    <constraint desc="" exp="" field="geometria_aproximada"/>
    <constraint desc="" exp="" field="tipo_pto_ref_geod_topo"/>
    <constraint desc="" exp="" field="tipo_marco_limite"/>
    <constraint desc="" exp="" field="rede_referencia"/>
    <constraint desc="" exp="" field="referencial_grav"/>
    <constraint desc="" exp="" field="situacao_marco"/>
    <constraint desc="" exp="" field="data_visita"/>
    <constraint desc="" exp="" field="valor_gravidade"/>
    <constraint desc="" exp="" field="possui_monografia"/>
    <constraint desc="" exp="" field="numero_fotos"/>
    <constraint desc="" exp="" field="possui_croqui"/>
    <constraint desc="" exp="" field="possui_arquivo_rastreio"/>
    <constraint desc="" exp="" field="endereco_imagem_lateral_1"/>
    <constraint desc="" exp="" field="endereco_imagem_lateral_2"/>
    <constraint desc="" exp="" field="endereco_imagem_lateral_3"/>
    <constraint desc="" exp="" field="endereco_imagem_lateral_4"/>
    <constraint desc="" exp="" field="endereco_imagem_aerea"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="&quot;possui_arquivo_rastreio&quot;" sortOrder="0">
    <columns>
      <column name="id" type="field" hidden="0" width="-1"/>
      <column name="cod_ponto" type="field" hidden="0" width="-1"/>
      <column name="data_rastreio" type="field" hidden="0" width="-1"/>
      <column name="tipo_ref" type="field" hidden="0" width="-1"/>
      <column name="latitude" type="field" hidden="0" width="-1"/>
      <column name="longitude" type="field" hidden="0" width="-1"/>
      <column name="norte" type="field" hidden="0" width="-1"/>
      <column name="leste" type="field" hidden="0" width="-1"/>
      <column name="altitude_ortometrica" type="field" hidden="0" width="-1"/>
      <column name="altitude_geometrica" type="field" hidden="0" width="-1"/>
      <column name="sistema_geodesico" type="field" hidden="0" width="-1"/>
      <column name="outra_ref_plan" type="field" hidden="0" width="-1"/>
      <column name="referencial_altim" type="field" hidden="0" width="-1"/>
      <column name="outro_ref_alt" type="field" hidden="0" width="-1"/>
      <column name="fuso" type="field" hidden="0" width="-1"/>
      <column name="meridiano_central" type="field" hidden="0" width="-1"/>
      <column name="tipo_situacao" type="field" hidden="0" width="-1"/>
      <column name="reserva" type="field" hidden="0" width="-1"/>
      <column name="lote" type="field" hidden="0" width="-1"/>
      <column name="latitude_planejada" type="field" hidden="0" width="-1"/>
      <column name="longitude_planejada" type="field" hidden="0" width="-1"/>
      <column name="medidor" type="field" hidden="0" width="-1"/>
      <column name="inicio_rastreio" type="field" hidden="0" width="-1"/>
      <column name="fim_rastreio" type="field" hidden="0" width="-1"/>
      <column name="classificacao_ponto" type="field" hidden="0" width="-1"/>
      <column name="observacao" type="field" hidden="0" width="-1"/>
      <column name="metodo_posicionamento" type="field" hidden="0" width="-1"/>
      <column name="ponto_base" type="field" hidden="0" width="-1"/>
      <column name="materializado" type="field" hidden="0" width="-1"/>
      <column name="altura_antena" type="field" hidden="0" width="-1"/>
      <column name="tipo_medicao_altura" type="field" hidden="0" width="-1"/>
      <column name="referencia_medicao_altura" type="field" hidden="0" width="-1"/>
      <column name="altura_objeto" type="field" hidden="0" width="-1"/>
      <column name="mascara_elevacao" type="field" hidden="0" width="-1"/>
      <column name="taxa_gravacao" type="field" hidden="0" width="-1"/>
      <column name="modelo_gps" type="field" hidden="0" width="-1"/>
      <column name="modelo_antena" type="field" hidden="0" width="-1"/>
      <column name="numero_serie_gps" type="field" hidden="0" width="-1"/>
      <column name="numero_serie_antena" type="field" hidden="0" width="-1"/>
      <column name="modelo_geoidal" type="field" hidden="0" width="-1"/>
      <column name="precisao_horizontal_esperada" type="field" hidden="0" width="-1"/>
      <column name="precisao_vertical_esperada" type="field" hidden="0" width="-1"/>
      <column name="freq_processada" type="field" hidden="0" width="-1"/>
      <column name="data_processamento" type="field" hidden="0" width="-1"/>
      <column name="orbita" type="field" hidden="0" width="-1"/>
      <column name="orgao_executante" type="field" hidden="0" width="-1"/>
      <column name="projeto" type="field" hidden="0" width="-1"/>
      <column name="engenheiro_responsavel" type="field" hidden="0" width="-1"/>
      <column name="crea_engenheiro_responsavel" type="field" hidden="0" width="-1"/>
      <column name="cpf_engenheiro_responsavel" type="field" hidden="0" width="-1"/>
      <column name="geometria_aproximada" type="field" hidden="0" width="-1"/>
      <column name="tipo_pto_ref_geod_topo" type="field" hidden="0" width="-1"/>
      <column name="tipo_marco_limite" type="field" hidden="0" width="-1"/>
      <column name="rede_referencia" type="field" hidden="0" width="-1"/>
      <column name="referencial_grav" type="field" hidden="0" width="-1"/>
      <column name="situacao_marco" type="field" hidden="0" width="-1"/>
      <column name="data_visita" type="field" hidden="0" width="-1"/>
      <column name="valor_gravidade" type="field" hidden="0" width="-1"/>
      <column name="possui_monografia" type="field" hidden="0" width="-1"/>
      <column name="numero_fotos" type="field" hidden="0" width="-1"/>
      <column name="possui_croqui" type="field" hidden="0" width="-1"/>
      <column name="possui_arquivo_rastreio" type="field" hidden="0" width="-1"/>
      <column name="endereco_imagem_lateral_1" type="field" hidden="0" width="101"/>
      <column name="endereco_imagem_lateral_2" type="field" hidden="0" width="-1"/>
      <column name="endereco_imagem_lateral_3" type="field" hidden="0" width="-1"/>
      <column name="endereco_imagem_lateral_4" type="field" hidden="0" width="-1"/>
      <column name="endereco_imagem_aerea" type="field" hidden="0" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
    geom = feature.geometry()
    control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="altitude_geometrica" editable="1"/>
    <field name="altitude_ortometrica" editable="1"/>
    <field name="altura_antena" editable="1"/>
    <field name="altura_objeto" editable="1"/>
    <field name="classificacao_ponto" editable="1"/>
    <field name="cod_ponto" editable="1"/>
    <field name="cpf_engenheiro_responsavel" editable="1"/>
    <field name="crea_engenheiro_responsavel" editable="1"/>
    <field name="data_processamento" editable="1"/>
    <field name="data_rastreio" editable="1"/>
    <field name="data_visita" editable="1"/>
    <field name="endereco_imagem_aerea" editable="1"/>
    <field name="endereco_imagem_lateral_1" editable="1"/>
    <field name="endereco_imagem_lateral_2" editable="1"/>
    <field name="endereco_imagem_lateral_3" editable="1"/>
    <field name="endereco_imagem_lateral_4" editable="1"/>
    <field name="engenheiro_responsavel" editable="1"/>
    <field name="fim_rastreio" editable="1"/>
    <field name="freq_processada" editable="1"/>
    <field name="fuso" editable="1"/>
    <field name="geometria_aproximada" editable="1"/>
    <field name="id" editable="1"/>
    <field name="inicio_rastreio" editable="1"/>
    <field name="latitude" editable="1"/>
    <field name="latitude_planejada" editable="1"/>
    <field name="leste" editable="1"/>
    <field name="longitude" editable="1"/>
    <field name="longitude_planejada" editable="1"/>
    <field name="lote" editable="1"/>
    <field name="mascara_elevacao" editable="1"/>
    <field name="materializado" editable="1"/>
    <field name="medidor" editable="1"/>
    <field name="meridiano_central" editable="1"/>
    <field name="metodo_posicionamento" editable="1"/>
    <field name="modelo_antena" editable="1"/>
    <field name="modelo_geoidal" editable="1"/>
    <field name="modelo_gps" editable="1"/>
    <field name="norte" editable="1"/>
    <field name="numero_fotos" editable="1"/>
    <field name="numero_serie_antena" editable="1"/>
    <field name="numero_serie_gps" editable="1"/>
    <field name="observacao" editable="1"/>
    <field name="orbita" editable="1"/>
    <field name="orgao_executante" editable="1"/>
    <field name="outra_ref_plan" editable="1"/>
    <field name="outro_ref_alt" editable="1"/>
    <field name="ponto_base" editable="1"/>
    <field name="possui_arquivo_rastreio" editable="1"/>
    <field name="possui_croqui" editable="1"/>
    <field name="possui_monografia" editable="1"/>
    <field name="precisao_horizontal_esperada" editable="1"/>
    <field name="precisao_vertical_esperada" editable="1"/>
    <field name="projeto" editable="1"/>
    <field name="rede_referencia" editable="1"/>
    <field name="referencia_medicao_altura" editable="1"/>
    <field name="referencial_altim" editable="1"/>
    <field name="referencial_grav" editable="1"/>
    <field name="reserva" editable="1"/>
    <field name="sistema_geodesico" editable="1"/>
    <field name="situacao_marco" editable="1"/>
    <field name="taxa_gravacao" editable="1"/>
    <field name="tipo_marco_limite" editable="1"/>
    <field name="tipo_medicao_altura" editable="1"/>
    <field name="tipo_pto_ref_geod_topo" editable="1"/>
    <field name="tipo_ref" editable="1"/>
    <field name="tipo_situacao" editable="1"/>
    <field name="valor_gravidade" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="altitude_geometrica" labelOnTop="0"/>
    <field name="altitude_ortometrica" labelOnTop="0"/>
    <field name="altura_antena" labelOnTop="0"/>
    <field name="altura_objeto" labelOnTop="0"/>
    <field name="classificacao_ponto" labelOnTop="0"/>
    <field name="cod_ponto" labelOnTop="0"/>
    <field name="cpf_engenheiro_responsavel" labelOnTop="0"/>
    <field name="crea_engenheiro_responsavel" labelOnTop="0"/>
    <field name="data_processamento" labelOnTop="0"/>
    <field name="data_rastreio" labelOnTop="0"/>
    <field name="data_visita" labelOnTop="0"/>
    <field name="endereco_imagem_aerea" labelOnTop="0"/>
    <field name="endereco_imagem_lateral_1" labelOnTop="0"/>
    <field name="endereco_imagem_lateral_2" labelOnTop="0"/>
    <field name="endereco_imagem_lateral_3" labelOnTop="0"/>
    <field name="endereco_imagem_lateral_4" labelOnTop="0"/>
    <field name="engenheiro_responsavel" labelOnTop="0"/>
    <field name="fim_rastreio" labelOnTop="0"/>
    <field name="freq_processada" labelOnTop="0"/>
    <field name="fuso" labelOnTop="0"/>
    <field name="geometria_aproximada" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="inicio_rastreio" labelOnTop="0"/>
    <field name="latitude" labelOnTop="0"/>
    <field name="latitude_planejada" labelOnTop="0"/>
    <field name="leste" labelOnTop="0"/>
    <field name="longitude" labelOnTop="0"/>
    <field name="longitude_planejada" labelOnTop="0"/>
    <field name="lote" labelOnTop="0"/>
    <field name="mascara_elevacao" labelOnTop="0"/>
    <field name="materializado" labelOnTop="0"/>
    <field name="medidor" labelOnTop="0"/>
    <field name="meridiano_central" labelOnTop="0"/>
    <field name="metodo_posicionamento" labelOnTop="0"/>
    <field name="modelo_antena" labelOnTop="0"/>
    <field name="modelo_geoidal" labelOnTop="0"/>
    <field name="modelo_gps" labelOnTop="0"/>
    <field name="norte" labelOnTop="0"/>
    <field name="numero_fotos" labelOnTop="0"/>
    <field name="numero_serie_antena" labelOnTop="0"/>
    <field name="numero_serie_gps" labelOnTop="0"/>
    <field name="observacao" labelOnTop="0"/>
    <field name="orbita" labelOnTop="0"/>
    <field name="orgao_executante" labelOnTop="0"/>
    <field name="outra_ref_plan" labelOnTop="0"/>
    <field name="outro_ref_alt" labelOnTop="0"/>
    <field name="ponto_base" labelOnTop="0"/>
    <field name="possui_arquivo_rastreio" labelOnTop="0"/>
    <field name="possui_croqui" labelOnTop="0"/>
    <field name="possui_monografia" labelOnTop="0"/>
    <field name="precisao_horizontal_esperada" labelOnTop="0"/>
    <field name="precisao_vertical_esperada" labelOnTop="0"/>
    <field name="projeto" labelOnTop="0"/>
    <field name="rede_referencia" labelOnTop="0"/>
    <field name="referencia_medicao_altura" labelOnTop="0"/>
    <field name="referencial_altim" labelOnTop="0"/>
    <field name="referencial_grav" labelOnTop="0"/>
    <field name="reserva" labelOnTop="0"/>
    <field name="sistema_geodesico" labelOnTop="0"/>
    <field name="situacao_marco" labelOnTop="0"/>
    <field name="taxa_gravacao" labelOnTop="0"/>
    <field name="tipo_marco_limite" labelOnTop="0"/>
    <field name="tipo_medicao_altura" labelOnTop="0"/>
    <field name="tipo_pto_ref_geod_topo" labelOnTop="0"/>
    <field name="tipo_ref" labelOnTop="0"/>
    <field name="tipo_situacao" labelOnTop="0"/>
    <field name="valor_gravidade" labelOnTop="0"/>
  </labelOnTop>
  <reuseLastValue>
    <field name="altitude_geometrica" reuseLastValue="0"/>
    <field name="altitude_ortometrica" reuseLastValue="0"/>
    <field name="altura_antena" reuseLastValue="0"/>
    <field name="altura_objeto" reuseLastValue="0"/>
    <field name="classificacao_ponto" reuseLastValue="0"/>
    <field name="cod_ponto" reuseLastValue="0"/>
    <field name="cpf_engenheiro_responsavel" reuseLastValue="0"/>
    <field name="crea_engenheiro_responsavel" reuseLastValue="0"/>
    <field name="data_processamento" reuseLastValue="0"/>
    <field name="data_rastreio" reuseLastValue="0"/>
    <field name="data_visita" reuseLastValue="0"/>
    <field name="endereco_imagem_aerea" reuseLastValue="0"/>
    <field name="endereco_imagem_lateral_1" reuseLastValue="0"/>
    <field name="endereco_imagem_lateral_2" reuseLastValue="0"/>
    <field name="endereco_imagem_lateral_3" reuseLastValue="0"/>
    <field name="endereco_imagem_lateral_4" reuseLastValue="0"/>
    <field name="engenheiro_responsavel" reuseLastValue="0"/>
    <field name="fim_rastreio" reuseLastValue="0"/>
    <field name="freq_processada" reuseLastValue="0"/>
    <field name="fuso" reuseLastValue="0"/>
    <field name="geometria_aproximada" reuseLastValue="0"/>
    <field name="id" reuseLastValue="0"/>
    <field name="inicio_rastreio" reuseLastValue="0"/>
    <field name="latitude" reuseLastValue="0"/>
    <field name="latitude_planejada" reuseLastValue="0"/>
    <field name="leste" reuseLastValue="0"/>
    <field name="longitude" reuseLastValue="0"/>
    <field name="longitude_planejada" reuseLastValue="0"/>
    <field name="lote" reuseLastValue="0"/>
    <field name="mascara_elevacao" reuseLastValue="0"/>
    <field name="materializado" reuseLastValue="0"/>
    <field name="medidor" reuseLastValue="0"/>
    <field name="meridiano_central" reuseLastValue="0"/>
    <field name="metodo_posicionamento" reuseLastValue="0"/>
    <field name="modelo_antena" reuseLastValue="0"/>
    <field name="modelo_geoidal" reuseLastValue="0"/>
    <field name="modelo_gps" reuseLastValue="0"/>
    <field name="norte" reuseLastValue="0"/>
    <field name="numero_fotos" reuseLastValue="0"/>
    <field name="numero_serie_antena" reuseLastValue="0"/>
    <field name="numero_serie_gps" reuseLastValue="0"/>
    <field name="observacao" reuseLastValue="0"/>
    <field name="orbita" reuseLastValue="0"/>
    <field name="orgao_executante" reuseLastValue="0"/>
    <field name="outra_ref_plan" reuseLastValue="0"/>
    <field name="outro_ref_alt" reuseLastValue="0"/>
    <field name="ponto_base" reuseLastValue="0"/>
    <field name="possui_arquivo_rastreio" reuseLastValue="0"/>
    <field name="possui_croqui" reuseLastValue="0"/>
    <field name="possui_monografia" reuseLastValue="0"/>
    <field name="precisao_horizontal_esperada" reuseLastValue="0"/>
    <field name="precisao_vertical_esperada" reuseLastValue="0"/>
    <field name="projeto" reuseLastValue="0"/>
    <field name="rede_referencia" reuseLastValue="0"/>
    <field name="referencia_medicao_altura" reuseLastValue="0"/>
    <field name="referencial_altim" reuseLastValue="0"/>
    <field name="referencial_grav" reuseLastValue="0"/>
    <field name="reserva" reuseLastValue="0"/>
    <field name="sistema_geodesico" reuseLastValue="0"/>
    <field name="situacao_marco" reuseLastValue="0"/>
    <field name="taxa_gravacao" reuseLastValue="0"/>
    <field name="tipo_marco_limite" reuseLastValue="0"/>
    <field name="tipo_medicao_altura" reuseLastValue="0"/>
    <field name="tipo_pto_ref_geod_topo" reuseLastValue="0"/>
    <field name="tipo_ref" reuseLastValue="0"/>
    <field name="tipo_situacao" reuseLastValue="0"/>
    <field name="valor_gravidade" reuseLastValue="0"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"cod_ponto"</previewExpression>
  <mapTip>&lt;style>&#xd;
.stilo_div {&#xd;
	text-align: center;&#xd;
	background-color: white;&#xd;
	width: 360px;&#xd;
	heigth: auto;&#xd;
}&#xd;
.link_foto {&#xd;
	background-color: black;&#xd;
	color: white;&#xd;
	padding: 11px 22px;&#xd;
	border-radius: 8px;&#xd;
	font-size: 12px;&#xd;
	text-decoration: none;&#xd;
	font-family: 'Roboto';&#xd;
	margin: auto;&#xd;
}&#xd;
.border-bottom {&#xd;
    border-bottom: 10px solid #73af00;&#xd;
    padding: 50px;&#xd;
    margin: 50px;&#xd;
}&#xd;
&#xd;
table, td {&#xd;
  margin: auto;&#xd;
  border: 1px solid black;&#xd;
  border-collapse: collapse;&#xd;
  padding: 22px 10px;&#xd;
  text-align: center;&#xd;
}&#xd;
&#xd;
th {&#xd;
  font-family:6px;&#xd;
  margin: auto;&#xd;
  border: 1px solid black;&#xd;
  border-collapse: collapse;&#xd;
  padding: 6px 3px;&#xd;
  text-align: center;&#xd;
}&#xd;
&#xd;
.body {&#xd;
  text-align: center;&#xd;
}&#xd;
&lt;/style>&#xd;
&#xd;
&lt;div class="stilo_div">&#xd;
		&lt;table>&#xd;
			&lt;thead>&#xd;
				&lt;tr>&#xd;
					&lt;th colspan="2">&lt;b>[% "cod_ponto" %]&lt;/b>&lt;/th>&#xd;
				&lt;/tr>&#xd;
			&lt;/thead>&#xd;
			&lt;tbody>&#xd;
				&lt;tr>&#xd;
					&lt;th>Fotografias&lt;/th>&#xd;
					&lt;th>Documentos&lt;/th>&#xd;
				&lt;/tr>&#xd;
				&lt;tr>&#xd;
					&lt;td>&lt;b>&lt;a href="[% "endereco_imagem_aerea" %]" class="link_foto" target="_blank">Imagem Aérea&lt;/a>&lt;/b>&lt;/td>&#xd;
					&lt;td>&lt;b>&lt;a href="[% "endereco_monografia" %]" class="link_foto" target="_blank">Monografia&lt;/a>&lt;/b>&lt;/td>&#xd;
				&lt;/tr>&#xd;
				&lt;tr>&#xd;
					&lt;td>&lt;b>&lt;a href="[% "endereco_imagem_lateral_1" %]" class="link_foto" target="_blank">Imagem Lateral [% string_to_array(file_name("endereco_imagem_lateral_1"), '_')[1] %] graus&lt;/a>&lt;/b>&lt;/td>&#xd;
					&lt;td>&lt;b>&lt;a href="[% "endereco_croqui" %]" class="link_foto" target="_blank">Croqui&lt;/a>&lt;/b>&lt;/td>&#xd;
				&lt;/tr>&#xd;
				&lt;tr>&#xd;
					&lt;td>&lt;b>&lt;a href="[% "endereco_imagem_lateral_2" %]" class="link_foto" target="_blank">Imagem Lateral [% string_to_array(file_name("endereco_imagem_lateral_2"), '_')[1] %] graus&lt;/a>&lt;/b>&lt;/td>&#xd;
					&lt;td>&lt;b>&lt;a href="[% "endereco_rinex" %]" class="link_foto" target="_blank">RINEX&lt;/a>&lt;/b>&lt;/td>&#xd;
				&lt;/tr>&#xd;
				&lt;tr>&#xd;
					&lt;td>&lt;b>&lt;a href="[% "endereco_imagem_lateral_3" %]" class="link_foto" target="_blank">Imagem Lateral [% string_to_array(file_name("endereco_imagem_lateral_3"), '_')[1] %] graus&lt;/a>&lt;/b>&lt;/td>&#xd;
					&lt;td>&lt;/td>&#xd;
				&lt;/tr>&#xd;
				&lt;tr>&#xd;
					&lt;td>&lt;b>&lt;a href="[% "endereco_imagem_lateral_4" %]" class="link_foto" target="_blank">Imagem Lateral [% string_to_array(file_name("endereco_imagem_lateral_4"), '_')[1] %] graus&lt;/a>&lt;/b>&lt;/td>&#xd;
					&lt;td>&lt;/td>&#xd;
				&lt;/tr>&#xd;
			&lt;/tbody>&#xd;
		&lt;/table>&#xd;
&lt;/div></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
