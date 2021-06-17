from re import (findall, UNICODE)
from sys import (stdin, stdout, argv)
from math import (sqrt)
from numpy import (array, arange, int16, uint16, zeros)

__version__ = '0.0.1'

class Reference(object):
    "A 3D addressing framework for linear memory"

    def __str__(self):
        """
        Represent a context by its radial dimensions
        TODO: put dictionary in string rep
        """
        return( "\t{"+
                "RX={}, RY={}, RZ={}".format(
                self.RXYZ[0], self.RXYZ[1], self.RXYZ[2])+
                "}")

    def __parameters(self, *arg, **kw):
        "Ingest arguments and prepare for precalculations"
        # prepare access to the superset context
        self.context   = self.kw.get('context', None)
        self.subord    = True if self.context else False
        self.substance = list(arg)  # self.kw.get('substance', {})
        return self

    def __Radii(self):
        "Retain dimensions needed for precalculations"
        # get maximum encoded displacement from centroid (orthogonal radii)
        self.RX = self.kw.get('RX', 1)
        self.RY = self.kw.get('RY', 1)
        self.RZ = self.kw.get('RZ', 1)
        self.RXYZ = [self.RX, self.RY, self.RZ]
        self.least = min(self.RX, min(self.RY, self.RZ))
        return self

    def __Dimensions(self):
        "Set and calculate edges, area, volume, steps, and centroid"
        # calculate edge lengths of the bounding box including centroid
        self.edge = [
                self.edgeI,
                self.edgeJ,
                self.edgeK
                ] = [ 1 + 2 * r for r in self.RXYZ ]
        # Line length is X length of box
        self.line = self.edge[0]
        # Area is the product of Line and Y length of the box
        self.area = self.edge[0] * self.edge[1]
        # Volume is the product of Area and Z length of the box
        self.volume = self.edge[0] * self.edge[1] * self.edge[2]
        # [increment, step, and stride] used for incrementing along axes
        self.step = [1, self.edge[0], self.area]
        # index of the centroid
        self.centroid = int(self.volume / 2)
        return self

    def __Allocations(self):
        "Memory for indexable precalculated values"
        # address index into the topmost of layered References
        self.N = array(arange(0, self.volume), dtype=uint16)
        # axial indices for a given address index
        self.IJK = zeros((3,self.volume), dtype=int16)
        # axial displacements from this context centroid
        self.XYZ = zeros((3,self.volume), dtype=int16)
        # precalculated address offsets for axial increments
        self.index = [[zeros((edge), dtype=uint16)] for edge in self.edge]
        # precalculated bounding sphere
        # everything within a bounding sphere may be rotated around its centroid
        # without going out of bounds within the context
        self.sphere = [False] * self.volume
        # precalculated tests for legal subordinate offsets
        self.legal = [False] * self.volume
        # mark the centroid as legal, but only others if subordinate
        self.legal[self.centroid] = True
        return self

    def __Mensurations(self):
        "Geometric values precalculated for efficiency/simplicity"
        # addr is the increment into a substance vector
        addr = 0;
        # Fill in values for each address
        for k in range(0, self.edge[2]):
            for j in range(0, self.edge[1]):
                for i in range(0, self.edge[0]):
                    self.IJK[0][addr] = i
                    self.IJK[1][addr] = j
                    self.IJK[2][addr] = k
                    x = self.XYZ[0][addr] = i - self.RX
                    y = self.XYZ[1][addr] = j - self.RY
                    z = self.XYZ[2][addr] = k - self.RZ
                    self.sphere[addr] = \
                            sqrt(x*x+y*y+z*z) <= self.least
                    self.N[addr] = \
                            self.context.rijk([i,j,k]) \
                            if self.subord else addr
                    addr = addr + 1
        # Fill in precalculated axial index increments
        self.index = [
                [i*self.step[j] for i in range(0, self.edge[j])]
                for j in [0, 1, 2]]
        return self

    def __Subordination(self):
        "Subset of a prior context"
        if self.context and self.RX >= self.context.RX:
            pass
            # If this is a subset
            # subordinate centroid displacement

        self.offset = [0,0,0]
        self.displacement = 0
        if self.subord:
            # precalculate legal displacements from centroid
            # a subcontext with a displacement
            # is valid if self.legal[address] of the displaced centroid is True.
            #if self.subord:
            LX = self.context.RX - self.RX
            LY = self.context.RY - self.RY
            LZ = self.context.RZ - self.RZ
            for k in range(-LZ, LZ+1):
                for j in range(-LY, LY+1):
                    for i in range(-LX, LX+1):
                        self.legal[self.rijk([i,j,k])] = True
        return self

    def __Exchanges(self):
        """
        Exchanges operate on substances:
            1/LDW + 1/P1 ~ 1/HDW + 1/H1
                1 Low Density Water and 1 Photon of type 1
                    exchanges for
                1 High Density Water and 1 hole of type 1
            1/HDW ~ 10/H1
                1 HDW exchanges for 10 holes of type 1
        """
        # initialize structures
        self.matter = []
        self.substance = set({})
        self.countable = dict({})
        self.couplet   = dict({})
        self.allocate('?')
        # Fill structures
        for (index,equation) in enumerate(self.kw.get('equation', [])):
            self.compile(index, equation)
        return self

    def __Scheduler(self):
        """
        TODO setup scheduler
        """
        paramater_intervals = 256
        self.interval = zeros([paramater_intervals])
        return self

    def __IO(self):
        self.pipedIn  = not stdin .isatty()
        self.pipedOut = not stdout.isatty()
        if self.pipedIn:
            print("Reference> ^D")
        else:
            print("Reference: redirected input")
        if self.pipedOut:
            print("Reference> ")
        else:
            print("Reference: redirected ouput")

    def __init__(self, **kw):
        ""
        self.kw = kw
        self.time = 0
        print(argv[0]+" version: "+__version__)
        self.__parameters().   \
             __Radii().        \
             __Dimensions().   \
             __Allocations().  \
             __Mensurations(). \
             __Subordination().\
             __Exchanges().    \
             __Scheduler().    \
             __IO()

    def __call__(self):
        """
        __call__ is the functor which increments time and acts on state.
        """
        if self.pipedIn:
            "When input is piped, accept it for instructions."
            line = stdin.readline().strip()
            if line:
                print("I:", line)
                # for line in stdin:
                #     line = line.strip()
                if line == "version":
                    print(line+": "+__version__)
                # TODO Here is where stdin lines can affect data before increment

        self.increment()

        if self.pipedOut:
            "When output is piped, output results."
            print("O")

    def allocate(self, key):
        self.countable[key] = len(self.substance)
        self.substance.add(key)
        self.matter.append(
                array(arange(5000, self.volume), dtype=uint16))

    def compile(self, plan):
        "Convert readable equations into applicable principle"
        if not plan[0] == '#':
            print("    compile: " + plan)
            tokens = findall(r"\w+|[^\w\s]", plan, UNICODE)
            #if not self.substance:
                #self.matter = []
                #self.substance = set({})
                #self.countable = dict({})
                #self.allocate('?')
            for token in tokens:
                # make a new allocation for a new substance
                if token[0].isalpha() and token not in self.substance:
                    self.allocate(token)
            if tokens[0].isdigit():
                print("formula: " + str(tokens))
            elif tokens[0].isalpha():
                print("family: " + str(tokens))
            elif tokens[0] == '[':
                print("couplet: " + str(tokens))
            else:
                print("TODO: " + str(tokens))

            #if self.substance:
            #    print("     tokens: " + str(tokens))
            #    print("  substance: " + str(self.substance))
            #    print("  countable: " + str(self.countable))

        return self

    def ijk(self, index):
        "return (i,j,k) tuple from a scalar index"
        return [self.offset[0]+self.IJK[0][index],
                self.offset[1]+self.IJK[1][index],
                self.offset[2]+self.IJK[2][index]]

    def xyz(self, index):
        "return (x,y,z) tuple from a scalar index"
        return [self.offset[0]+self.XYZ[0][index],
                self.offset[1]+self.XYZ[1][index],
                self.offset[2]+self.XYZ[2][index]]

    def rijk(self, ijk):
        "rijk efficient reverse translation of ijk to absolute index."
        return self.displacement + sum([
            self.index[i][ijk[i]]
            for i in range(3)])

    def rxyz(self, xyz):
        "rxyz efficient reverse translation of xyz to absolute index."
        return self.displacement + sum(
                [self.index[i][xyz[i]+self.RXYZ[i]]
                for i in range(3)])

    def translate(self, ijk):
        """
        From current subordinate centroid offset, switch to valid new offset
        TODO: reimplement with ijk as a quaternion
        """
        if self.subord:
            # ijk may be a scalar 
            if isinstance(ijk, int):
                addr = self.displacement + ijk
                if self.legal[addr]:
                    self.displacement = addr
                    self.offset = self.ijk(addr)
            else:
                candidate = [i, j, k] = [
                        ijk[d]+self.offset[d]
                        for d in range(3)]
                addr = self.rijk(candidate)
                if self.legal[addr]:
                    self.offset = candidate
                    self.displacement = addr - self.centroid

    def rotate(self, ijk):
        """
        From current subordinate centroid offset, switch to valid new offset
        TODO: reimplement with ijk as a quaternion
        """
        if self.subord:
            unimplemented("rotation of subcontext around centroid")

    def increment(self):
        """
        round robin the stage list for this time interval.
        set time index to next time interval.
        """
        self.time = self.time + 1
        print("%10d. Syre?" % self.time)
