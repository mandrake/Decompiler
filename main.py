import sublime, sublime_plugin
import pymsasid.pymsasid as pydasm

class DecompileCommand(sublime_plugin.TextCommand):
    def asm_print(self, inst, prog):
        branch = inst.branch()
        while (len(branch) == 1):
            s = '[' + hex (prog.pc) + '] '
            inst = prog.disassemble (branch[0])
            self.asm_out.write(s + str (inst) + '\n')
            print (s + str (inst))
            branch = inst.branch()

        if (len(branch) == 2):
            if branch[0] not in self.branches:
                self.branches.append(branch[0])
                print "New Branch L"
                self.asm_out.write("New Branch L\n")
                self.asm_print(prog.disassemble(branch[0]), prog)
            if branch[1] not in self.branches:
                self.branches.append(branch[1])
                print "New Branch R"
                self.asm_out.write("New Branch R\n")
                self.asm_print(prog.disassemble(branch[1]), prog)

    def run(self, edit):
        self.branches = []
        self.asm_out = open(os.path.dirname(self.view.file_name())+'\\asm.out', 'w')
        prog = pydasm.Pymsasid(hook=pydasm.PEFileHook, source=self.view.file_name())
        inst = prog.disassemble(prog.pc)
        self.asm_print(inst, prog)
        close(self.asm_out)
        # app = QtCore.CoreApplication([])
        # launch_process()
        # app.exec_()