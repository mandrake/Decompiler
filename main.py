import sublime, sublime_plugin
import pymsasid.pymsasid as pydasm
import os
import view

class DecompileCommand(sublime_plugin.TextCommand):
    def hurr_durr_buffehr(self, file_name):
        buf = []
        with open(file_name, "rb") as bin:
            b = bin.read(1)
            while b:
                buf.append(b)
                b = bin.read(1)

        return buf

    def hurr_durr_printor(self, inst, prog):
        branch = inst.branch()
        while (len(branch) == 1):
            s = '[' + hex (prog.pc) + '] '
            inst = prog.disassemble (branch[0])
            self.culo.write(s + str (inst) + '\n')
            print (s + str (inst))
            branch = inst.branch()

        if (len(branch) == 2):
            if branch[0] not in self.branches:
                self.branches.append(branch[0])
                print "New Branch L"
                self.culo.write("New Branch L\n")
                self.hurr_durr_printor(prog.disassemble(branch[0]), prog)
            if branch[1] not in self.branches:
                self.branches.append(branch[1])
                print "New Branch R"
                self.culo.write("New Branch R\n")
                self.hurr_durr_printor(prog.disassemble(branch[1]), prog)

    def run(self, edit):
        self.branches = []
        self.culo = open(os.path.dirname(self.view.file_name())+'\disasm', 'w')
        prog = pydasm.Pymsasid(hook=pydasm.PEFileHook, source=self.view.file_name())
        inst = prog.disassemble(prog.pc)
        app = QtCore.CoreApplication([])
        launch_process()
        app.exec_()
        #self.hurr_durr_printor(inst, prog)