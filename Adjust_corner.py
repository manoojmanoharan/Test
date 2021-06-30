import nuke
import nukescripts

vd = {'x': 1, 'y': 1, 'r': 1, 't': 1}


def set_knob_default(reformat, crop):
    """
    This function set default value for crop node
    :param reformat: value for reformat knob
    :type reformat: string
    :param crop: value for crop knob
    :type crop: sting
    """
    nuke.knobDefault('Crop.reformat', reformat)
    nuke.knobDefault('Crop.crop', crop)


def set_animated_to(node):
    """
    this function wills set to knobs in corner pin node to animated
    :param node: Pass the node object, usually selected node
    :type node: node object
    """
    for i in range(1, 5):
        node.knob('to{}'.format(i)).setAnimated()


def clear_from_animation(node):
    """
    This function clears animation from the from knob in corner pin  node
    :param node: Pass the node object, usually selected node
    :type node: node object
    """
    for i in range(1, 5):
        node.knob('from{}'.format(i)).clearAnimated()


def set_value_to(node, to, x_k, y_k):
    """
    This function set values in to knobs in corner pin node
    :param node: Pass the node object, usually selected node
    :type node: node object
    :param to: name of the to knob
    :type to: string
    :param x_k: x value of the to knob
    :type x_k: integer
    :param y_k: y value of the to knob
    :type y_k: integer
    """
    node['{}'.format(to)].setValue(x_k, 0)
    node['{}'.format(to)].setValue(y_k, 1)


def get_box_value(node, num):
    """
    this function gets the box value from the crop node
    :param node: Pass the node object, usually selected node
    :type node: node object
    :param num: index of the knob
    :type num: integer
    :return: Returns the value of the corresponding knob
    :rtype: integer
    """
    return node['box'].getValue(num)


def run_this():
    """
    This is the main function, run this to run the tool
    """
    set_knob_default(reformat='0', crop='1')
    n = nuke.selectedNode()
    f = nuke.frame()
    nukescripts.autocrop(first=f, last=f)
    dep_node = n.dependent()[0]
    set_knob_default(reformat='1', crop='0')

    for idx, (key, value) in enumerate(vd.items()):
        vd[key] = get_box_value(node=dep_node, num=idx)

    nuke.delete(dep_node)
    c = nuke.nodes.CornerPin2D(name="Adjust_corner")
    c.setInput(0, n)
    set_animated_to(node=c)
    set_value_to(node=c, to='to1', x_k=vd['x'], y_k=vd['y'])
    set_value_to(node=c, to='to2', x_k=vd['x'], y_k=vd['t'])
    set_value_to(node=c, to='to3', x_k=vd['r'], y_k=vd['y'])
    set_value_to(node=c, to='to4', x_k=vd['r'], y_k=vd['t'])
    c.knob('copy_to').execute()
    set_animated_to(node=c)
    clear_from_animation(node=c)


run_this()


********************************************************************

import nuke
import nukescripts



def adjustCorner():
	par = nuke.selectedNode()



	nuke.knobDefault('Crop.reformat','0')
	nuke.knobDefault('Crop.crop','1')

	n = nuke.selectedNode()
	f = nuke.frame()
	nukescripts.autocrop(first=f,last=f)
	dep_node = n.dependent()[0]
	dep_node['selected'].setValue(True)
	nuke.knobDefault('Crop.reformat','1')
	nuke.knobDefault('Crop.crop','0')

	x=nuke.selectedNode()['box'].getValue(0)
	y=nuke.selectedNode()['box'].getValue(1)
	r=nuke.selectedNode()['box'].getValue(2)
	t=nuke.selectedNode()['box'].getValue(3)

	nuke.delete(nuke.selectedNode())




	c = nuke.nodes.CornerPin2D(name="Adjust_corner")
	c.setInput(0, par)

	c.knob('to1').setAnimated()
	c.knob('to2').setAnimated()
	c.knob('to3').setAnimated()
	c.knob('to4').setAnimated()

	c['to1'].setValue(x,0)
	c['to1'].setValue(y,1)
	c['to2'].setValue(x,0)
	c['to2'].setValue(t,1)
	c['to3'].setValue(r,0)
	c['to3'].setValue(y,1)
	c['to4'].setValue(r,0)
	c['to4'].setValue(t,1)

	c.knob('copy_to').execute()
	c.knob('to1').setAnimated()
	c.knob('to2').setAnimated()
	c.knob('to3').setAnimated()
	c.knob('to4').setAnimated()
	c.knob('from1').clearAnimated()
	c.knob('from2').clearAnimated()
	c.knob('from3').clearAnimated()
	c.knob('from4').clearAnimated()




#end script




# --------------------------------------------------------------
# adding menu and shortcut  ::::::::::::::::::::::::::::::::::
# --------------------------------------------------------------
EfficiencyMenu = nuke.menu('Nuke')
EfficiencyMenu.addCommand('Efficiency/Adjust_corner', 'Adjust_corner.adjustCorner()','F3')
