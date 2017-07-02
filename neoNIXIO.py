# Ajayrama Kumaraswamy, 2016
# Ginjang Project, LMU

import nixio as nix
import neo
import quantities as qu
import numpy as np

qu2Val = lambda x: nix.Value(float(x))
quUnitStr = lambda x: x.dimensionality.string

#***********************************************************************************************************************

def addAnalogSignal2Block(blk, analogSignal):
    '''
    Create a new data array in the block blk and add the data in analogSignal to it
    :param blk: nix.block
    :param analogSignal: neo.analogsignal
    :return: data, nix.data_array, the newly added data_array
    '''

    assert hasattr(analogSignal, 'name'), 'Analog signal has no name'

    data = blk.create_data_array(analogSignal.name, 'nix.regular_sampled', data=analogSignal.magnitude)

    data.unit = quUnitStr(analogSignal)
    data.label = analogSignal.name

    qu.set_default_units = 'SI'
    samplingPeriod = analogSignal.sampling_period.simplified
    t = data.append_sampled_dimension(float(samplingPeriod))
    t.label = 'time'
    t.unit = quUnitStr(samplingPeriod)
    t.offset = float(analogSignal.t_start.simplified)

    return data

#***********************************************************************************************************************

def dataArray2AnalogSignal(dataArray):
    '''
    Convert a nix data_array into a neo analogsignal
    :param dataArray: nix.data_array
    :return: neo.analogsignal
    '''

    assert len(dataArray.dimensions) == 1, 'Only one dimensional arrays are supported'
    dim = dataArray.dimensions[0]
    assert isinstance(dim, nix.pycore.SampledDimension), 'Only Sampled Dimensions' \
                                                         'are supported'

    t_start = qu.Quantity(dim.offset, units=dim.unit)
    samplingPeriod = qu.Quantity(dim.sampling_interval, units=dim.unit)

    analogSignal = neo.AnalogSignal(signal=np.array(dataArray[:]),
                                    units=dataArray.unit,
                                    sampling_period=samplingPeriod,
                                    t_start=t_start)

    analogSignal.name = dataArray.name

    return analogSignal

#***********************************************************************************************************************

def property2qu(property):
    '''
    Convert a nix property to a quantities Quantity
    :param property: nix.property
    :return: quantities.Quantity
    '''

    return qu.Quantity([v.value for v in property.values], units=property.unit)

#***********************************************************************************************************************

def addQuantity2section(sec, quant, name):
    '''
    Create new property in section sec and add the data in quantity.Quantitiy quant to it
    :param sec: nix.section
    :param quant: quantities.Quantity
    :param name: name of the property to add
    :return: p, nix.property, the property added.
    '''

    if quant.shape == ():

        p = sec.create_property(name, [qu2Val(quant)])

    #only 1D arrays
    elif len(quant.shape) == 1:

        #not an empty 1D array
        if quant.shape[0]:

            p = sec.create_property(name, [qu2Val(x) for x in quant])

        else:
            raise(ValueError('Quantity passed must be either scalar or 1 dimensional'))

    else:
            raise(ValueError('Quantity passed must be either scalar or 1 dimensional'))

    p.unit = quUnitStr(quant)

    return p

#***********************************************************************************************************************

def createPosDA(name, pos, blk):
    '''
    Create a data_array of type 'nix.positions' with the pos data in the block blk
    :param name: string, name of the data_array to create
    :param pos: iterable of floats, data to be added to the created data_array
    :param blk: nix.block, the block in which the data_array is to be created
    :return: positions, nix.data_array, the newly created data_array
    '''

    positions = blk.create_data_array(name, 'nix.positions', data=pos)
    positions.append_set_dimension()
    positions.append_set_dimension()

    return positions

#***********************************************************************************************************************

def createExtDA(name, ext, blk):
    '''
   Create a data_array of type 'nix.extents' with the pos data in the block blk
   :param name: string, name of the data_array to create
   :param ext: iterable of floats, data to be added to the created data_array
   :param blk: nix.block, the block in which the data_array is to be created
   :return: extents, nix.data_array, the newly created data_array
   '''

    extents = blk.create_data_array(name, 'nix.extents', data=ext)
    extents.append_set_dimension()
    extents.append_set_dimension()

    return extents

#***********************************************************************************************************************

def tag2AnalogSignal(tag, refInd):
    '''
    Create a neo.analogsignal from the snippet of data represented by a nix.tag and its reference at index refInd
    :param tag: nix.tag
    :param refInd: the index of the reference among those of the tag to use
    :return: neo.analogsignal with the snipped of reference data tagged by tag.
    '''

    ref = tag.references[refInd]
    dim = ref.dimensions[0]
    offset = dim.offset
    ts = dim.sampling_interval
    nSamples = ref[:].shape[0]

    startInd = max(0, int(np.floor((tag.position[0] - offset) / ts)))
    endInd = min(startInd + int(np.floor(tag.extent[0] / ts)) + 1, nSamples)
    trace = ref[startInd:endInd]

    analogSignal = neo.AnalogSignal(signal=trace,
                                    units=ref.unit,
                                    sampling_period=qu.Quantity(ts, units=dim.unit),
                                    t_start=qu.Quantity(offset + startInd * ts, units=dim.unit))

    analogSignal = analogSignal.reshape((analogSignal.shape[0],))
    # trace = tag.retrieve_data(refInd)[:]
    # tVec = tag.position[0] + np.linspace(0, tag.extent[0], trace.shape[0])

    return analogSignal

#***********************************************************************************************************************

def getTagPosExt(tag):

    position = tag.position[0] * qu.Quantity(1, units=tag.units[0])
    extent = tag.extent[0] * qu.Quantity(1, units=tag.units[0])

    return position, extent



#***********************************************************************************************************************
def multiTag2SpikeTrain(tag, tStart, tStop):
    '''
    Create a neo.spiketrain from nix.multitag
    :param tag: nix.multitag
    :param tStart: float, time of start of the spike train in units of the multitag
    :param tStop: float, time of stop of the spike train in units of the multitag
    :return: neo.spiketrain
    '''


    if len(tag.positions):
        sp = neo.SpikeTrain(times=tag.positions[:], t_start=tStart, t_stop=tStop, units=tag.units[0])
    else:
        sp = neo.SpikeTrain(times=[], t_start=tStart, t_stop=tStop, units=qu.s)

    return sp


#***********************************************************************************************************************

def addMultiTag(name, type, positions, blk, refs, metadata=None, extents=None):
    '''
    Add a multi_tag to one or more data_arrays
    :param name: string, name of the multi_tag
    :param type: string, type of the multi_tag
    :param positions: quantities.Quantity, positions of the multi_tag
    :param blk: nix.Block, the block in which the multi_tag is to be created
    :param refs: list, list of nix.data_array objects, to which the multi_tag refers
    :param metadata: nix.Section, to which the the multi_tag refers
    :param extents: nix.data_array, extents of the multi_tag
    :return: nix.multi_tag, the newly created multi_tag
    '''

    refUnits0 = refs[0].dimensions[0].unit
    for ref in refs:
        assert len(ref.dimensions) == 1, 'Only 1D refs are supported for now.'
        assert ref.dimensions[0].unit == refUnits0, 'refs must have same time units'

    positionsUnitsNormed = simpleFloat(positions / qu.Quantity(1, units=refUnits0))
    positionsDA = createPosDA('{}_DA'.format(name), positionsUnitsNormed, blk)
    tag = blk.create_multi_tag(name, type, positionsDA)
    tag.units = [str(refUnits0)]

    if extents is not None:
        tag.extents = extents

    for ref in refs:
        tag.references.append(ref)

    if metadata is not None:
        tag.metadata = metadata

#***********************************************************************************************************************

def addTag(name, type, position, blk, refs, metadata=None, extent=None):
    '''
    Add a tag to one or more data_arrays
    :param name: string, name of the tag
    :param type: string, type of the tag
    :param position: float, position of the tag
    :param blk: nix.Block, the block in which the multi_tag is to be created
    :param refs: list, list of nix.data_array objects, to which the multi_tag refers
    :param metadata: nix.Section, to which the the multi_tag refers
    :param extent: float, extent of the multi_tag
    :return: nix.tag, the newly created tag
    '''
    tag = blk.create_tag(name, type, [position])



    if extent is not None:
        tag.extent = [extent]

    for ref in refs:
        tag.references.append(ref)
        tag.units = [str(ref.dimensions[0].unit)]

    if metadata is not None:
        tag.metadata = metadata


#***********************************************************************************************************************

def simpleFloat(quant):
    '''
    Float or List of float(s) of simplified version of a quantity that can be
    effectively represented as a float or list of floats.
    :param quant: a quantity.Quantity or an iterable of quantity.Quantity objects
    :return: float or iterable of floats depending on the argument quant
    '''

    # one element quantity
    if quant.shape == ():

        return float(quant.simplified)

    # 1D quantity
    elif len(quant.shape) == 1:

        if quant.shape[0]:

            return quant.simplified.magnitude.tolist()

        else:

            return []

    # 2D quantity
    elif len(quant.shape) == 2:

        if quant.shape[0]:

            # 2D column quantity
            if quant.shape[1] == 1:
                return quant.simplified.magnitude[:, 0].tolist()

            # 2D row quantity
            if quant.shape[0] == 1:
                return quant.simplified.magnitude[0, :].tolist()

            else:
                raise (TypeError('simpleFloat only supports scalar, '
                                 '1D, 2D row and 2D column quantities'))
        else:
            return []

    else:

        raise(TypeError('simpleFloat only supports scalar, '
                        '1D, 2D row and 2D column quantities'))

#***********************************************************************************************************************
