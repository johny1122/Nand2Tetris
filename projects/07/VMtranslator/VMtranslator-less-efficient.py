# project 7
#  This VMtranslator just copy the right command translation each time (with code duplication),
#   so is good for short vm programs.

import sys
import re
import os
import ntpath


HACK_COMMANDS_TRANSLATION = {
    #  Arithmetic / Logical commands
    "add": "@SP    // D=*SP    \n"
           "M=M-1	// SP--    \n"
           "A=M                \n"
           "D=M                \n"
           "                   \n"
           "@SP                \n"
           "M=M-1   // SP--    \n"
           "A=M                \n"
           "M=D+M   // *SP=D+M \n"
           "                   \n"
           "@SP    // SP++     \n"
           "M=M+1              \n",

    "sub": "@SP	// D=*SP        \n"
           "M=M-1	// SP--     \n"
           "A=M                 \n"
           "D=-M                \n"
           "                    \n"
           "@SP                 \n"
           "M=M-1	// SP--     \n"
           "A=M                 \n"
           "M=D+M	// *SP=D+M  \n"
           "                    \n"
           "@SP		// SP++     \n"
           "M=M+1               \n",

    "neg": "@SP		// D=*SP    \n"
           "M=M-1	// SP--		\n"
           "A=M					\n"
           "M=-M				\n"
           "                    \n"
           "@SP					\n"
           "M=M+1	// SP++		\n",

    "eq": "@SP				          \n"
          "M=M-1	// SP--		      \n"
          "A=M						  \n"
          "D=M	// D=*SP			  \n"
          "                           \n"
          "@SP						  \n"
          "M=M-1	// SP--		      \n"
          "A=M						  \n"
          "D=D-M	        	      \n"
          "                           \n"
          "@IF_EQUAL*XXX*	          \n"
          "D;JEQ				      \n"
          "@SP		// if not equal	  \n"
          "A=M						  \n"
          "M=0		// *SP=false	  \n"
          "@GOTO_END*XXX*		      \n"
          "0;JMP				      \n"
          "                           \n"
          "(IF_EQUAL*XXX*)// if equal \n"
          "@SP						  \n"
          "A=M						  \n"
          "M=-1		// *SP=true		  \n"
          "                           \n"
          "(GOTO_END*XXX*)			  \n"
          "@SP		// SP++			  \n"
          "M=M+1					  \n",

    "gt":   "@SP						    				\n"
            "M=M-1	// SP--			   						\n"
            "A=M						    				\n"
            "D=M		// D=*SP (y)	    				\n"
            "                                               \n"
            "@y												\n"
            "M=D											\n"
            "                                               \n"
            "@SP						    				\n"
            "M=M-1	// SP--			    					\n"
            "A=M						    				\n"
            "D=M		// D=*SP (x)	    				\n"
            "                                               \n"
            "@x												\n"
            "M=D											\n"
            "                                               \n"
            "@IF_X_POSITIVE*XXX*	//x>0					\n"
            "D;JGT											\n"
            "@IF_X_NEGATIVE_OR_ZERO*XXX*	//x<=0			\n"
            "0;JMP											\n"
            "                                               \n"
            "                                               \n"
            "(IF_X_POSITIVE*XXX*)							\n"
            "@y												\n"
            "D=M											\n"
            "                                               \n"
            "@IF_X_AND_Y_POS*XXX*		//x&y>0				\n"
            "D;JGT	//y>0									\n"
            "                                               \n"
            "@IF_TRUE*XXX*	//x>0 & y<=0					\n"
            "0;JMP											\n"
            "                                               \n"
            "(IF_X_AND_Y_POS*XXX*)							\n"
            "@x												\n"
            "D=M											\n"
            "@y												\n"
            "D=M-D	//D=y-x									\n"
            "@IF_FALSE*XXX*	//y-x>=0 == x<=y				\n"
            "D;JGE											\n"
            "@IF_TRUE*XXX*	//y-x<0 == x>y					\n"
            "0;JMP											\n"
            "                                               \n"
            "(IF_X_NEGATIVE_OR_ZERO*XXX*)					\n"
            "@y												\n"
            "D=M											\n"
            "@IF_X_AND_Y_ARE_NEG_OR_ZERO*XXX*	//x&y<=0	\n"
            "D;JLE	//y<=0									\n"
            "                                               \n"
            "@IF_FALSE*XXX*	//x<=0 & y>0					\n"
            "0;JMP											\n"
            "                                               \n"
            "(IF_X_AND_Y_ARE_NEG_OR_ZERO*XXX*)				\n"
            "@x												\n"
            "D=M											\n"
            "@y												\n"
            "D=M-D	//D=y-x									\n"
            "@IF_TRUE*XXX*	//y-x<0 == y<x					\n"
            "D;JLT											\n"
            "@IF_FALSE*XXX*	//y-x>=0 == y>=x				\n"
            "0;JMP											\n"
            "                                               \n"
            "(IF_TRUE*XXX*)		//if x>y				    \n"
            "@SP		   									\n"
            "A=M						    				\n"
            "M=-1			// *SP=true						\n"
            "@GOTO_END*XXX*			    					\n"
            "0;JMP											\n"
            "                                               \n"
            "(IF_FALSE*XXX*)		//if x<=y				\n"
            "@SP		   									\n"
            "A=M						    				\n"
            "M=0				// *SP=false				\n"
            "                                               \n"
            "(GOTO_END*XXX*)			    				\n"
            "@SP		// SP++			    				\n"
            "M=M+1					    					\n",

    "lt":   "@SP						    				\n"
            "M=M-1	// SP--			   						\n"
            "A=M						    				\n"
            "D=M		// D=*SP (y)	    				\n"
            "                                               \n"
            "@y												\n"
            "M=D											\n"
            "                                               \n"
            "@SP						    				\n"
            "M=M-1	// SP--			    					\n"
            "A=M						    				\n"
            "D=M		// D=*SP (x)	    				\n"
            "                                               \n"
            "@x												\n"
            "M=D											\n"
            "                                               \n"
            "@IF_X_POSITIVE*XXX*	//x>0					\n"
            "D;JGT											\n"
            "@IF_X_NEGATIVE_OR_ZERO*XXX*	//x<=0			\n"
            "0;JMP											\n"
            "                                               \n"
            "                                               \n"
            "(IF_X_POSITIVE*XXX*)							\n"
            "@y												\n"
            "D=M											\n"
            "                                               \n"
            "@IF_X_AND_Y_POS*XXX*		//x&y>0				\n"
            "D;JGT	//y>0									\n"
            "                                               \n"
            "@IF_FALSE*XXX*	//x>0 & y<=0					\n"
            "0;JMP											\n"
            "                                               \n"
            "(IF_X_AND_Y_POS*XXX*)							\n"
            "@x												\n"
            "D=M											\n"
            "@y												\n"
            "D=M-D	//D=y-x									\n"
            "@IF_TRUE*XXX*	//y-x>0 == x<y					\n"
            "D;JGT											\n"
            "@IF_FALSE*XXX*	//y-x<=0 == x>=y				\n"
            "0;JMP											\n"
            "                                               \n"
            "(IF_X_NEGATIVE_OR_ZERO*XXX*)					\n"
            "@y												\n"
            "D=M											\n"
            "@IF_X_AND_Y_ARE_NEG_OR_ZERO*XXX*	//x&y<=0	\n"
            "D;JLE	//y<=0									\n"
            "                                               \n"
            "@IF_TRUE*XXX*	//x<=0 & y>0					\n"
            "0;JMP											\n"
            "                                               \n"
            "(IF_X_AND_Y_ARE_NEG_OR_ZERO*XXX*)				\n"
            "@x												\n"
            "D=M											\n"
            "@y												\n"
            "D=M-D	//D=y-x									\n"
            "@IF_TRUE*XXX*	//y-x>0 == x<y					\n"
            "D;JGT											\n"
            "@IF_FALSE*XXX*	//y-x<=0 == x>=y				\n"
            "0;JMP											\n"
            "                                               \n"
            "(IF_TRUE*XXX*)		//if x<y					\n"
            "@SP		   									\n"
            "A=M						    				\n"
            "M=-1			// *SP=true						\n"
            "@GOTO_END*XXX*			    					\n"
            "0;JMP											\n"
            "                                               \n"
            "(IF_FALSE*XXX*)		//if x>=y				\n"
            "@SP		   									\n"
            "A=M						    				\n"
            "M=0				// *SP=false				\n"
            "                                               \n"
            "(GOTO_END*XXX*)			    				\n"
            "@SP		// SP++			    				\n"
            "M=M+1					    					\n",

    "and": "@SP						\n"
           "M=M-1	// SP--			\n"
           "A=M						\n"
           "D=M		// D=*SP		\n"
           "                        \n"
           "@SP						\n"
           "M=M-1	// SP--			\n"
           "A=M						\n"
           "M=D&M	//M = D and M	\n"
           "                        \n"
           "@SP		// SP++			\n"
           "M=M+1					\n",

    "or": "@SP						\n"
          "M=M-1	// SP--			\n"
          "A=M						\n"
          "D=M		// D=*SP		\n"
          "                         \n"
          "@SP						\n"
          "M=M-1	// SP--			\n"
          "A=M						\n"
          "M=D|M	// M = D or M	\n"
          "                         \n"
          "@SP		// SP++			\n"
          "M=M+1					\n",

    "not": "@SP						\n"
           "M=M-1	// SP--			\n"
           "A=M						\n"
           "M=!M	// *SP= not M	\n"
           "                        \n"
           "@SP	// SP++		    	\n"
           "M=M+1					\n",

    # PUSH - Memory commands

    "push constant": "D=A	//D = i     	 \n"
                     "                       \n"
                     "@SP					 \n"
                     "A=M					 \n"
                     "M=D	//*SP = D		 \n"
                     "                       \n"
                     "@SP	// SP++		     \n"
                     "M=M+1				     \n",

    "push local": "D=A     //D=i        \n"
                  "                     \n"
                  "@LCL                 \n"
                  "D=M+D   //D=LCL+i    \n"
                  "A=D                  \n"
                  "D=M     //D=*(LCL+i) \n"
                  "                     \n"
                  "@SP					\n"
                  "A=M					\n"
                  "M=D		//*SP = D	\n"
                  "                     \n"
                  "@SP		// SP++		\n"
                  "M=M+1				\n",

    "push argument": "D=A     //D=i       \n"
                     "                    \n"
                     "@ARG                \n"
                     "D=M+D   //D=ARG+i   \n"
                     "A=D                 \n"
                     "D=M     //D=*(ARG+i)\n"
                     "                    \n"
                     "@SP                 \n"
                     "A=M                 \n"
                     "M=D    //*SP = D	  \n"
                     "                    \n"
                     "@SP		// SP++	  \n"
                     "M=M+1				  \n",

    "push this": "D=A     //D=i        \n"
                 "                     \n"
                 "@THIS                \n"
                 "D=M+D   //D=THIS+i   \n"
                 "A=D                  \n"
                 "D=M     //D=*(THIS+i)\n"
                 "                     \n"
                 "@SP				   \n"
                 "A=M				   \n"
                 "M=D		//*SP = D  \n"
                 "                     \n"
                 "@SP		// SP++	   \n"
                 "M=M+1				   \n",

    "push that": "D=A     //D=i        \n"
                 "                     \n"
                 "@THAT                \n"
                 "D=M+D   //D=THAT+i   \n"
                 "A=D                  \n"
                 "D=M     //D=*(THAT+i)\n"
                 "                     \n"
                 "@SP				   \n"
                 "A=M				   \n"
                 "M=D		//*SP = D  \n"
                 "                     \n"
                 "@SP		// SP++	   \n"
                 "M=M+1				   \n",

    "push temp": "D=A     //D=i        \n"
                 "                     \n"
                 "@5                   \n"
                 "D=A+D   //D=5+i      \n"
                 "A=D                  \n"
                 "D=M     //D=*(5+i)   \n"
                 "                     \n"
                 "@SP				   \n"
                 "A=M				   \n"
                 "M=D		//*SP = D  \n"
                 "                     \n"
                 "@SP		// SP++	   \n"
                 "M=M+1				   \n",

    "push pointer": "D=A     //D=0/1            \n"
                    "                           \n"
                    "@IF_THIS*XXX*              \n"
                    "D;JEQ                      \n"
                    "                           \n"
                    "@THAT   //if that (1)      \n"
                    "D=M                        \n"
                    "@END*XXX*                  \n"
                    "0;JMP                      \n"
                    "                           \n"
                    "(IF_THIS*XXX*)   // (0)    \n"
                    "@THIS                      \n"
                    "D=M                        \n"
                    "                           \n"
                    "(END*XXX*)                 \n"
                    "@SP				        \n"
                    "A=M				        \n"
                    "M=D		//*SP = D       \n"
                    "                           \n"
                    "@SP		// SP++	        \n"
                    "M=M+1				        \n",

    "push static": "D=M     //D=foo.i   \n"
                   "                    \n"
                   "@SP					\n"
                   "A=M					\n"
                   "M=D		//*SP = D	\n"
                   "                    \n"
                   "@SP		// SP++		\n"
                   "M=M+1				\n",

    # POP - Memory commands

    "pop local": "D=A     //D=i           \n"
                 "                        \n"
                 "@LCL                    \n"
                 "D=M+D   //D=LCL+i       \n"
                 "                        \n"
                 "@save_address           \n"
                 "M=D                     \n"
                 "                        \n"
                 "@SP 				      \n"
                 "M=M-1   // SP--         \n"
                 "A=M					  \n"
                 "D=M	//D = *SP	      \n"
                 "                        \n"
                 "@save_address           \n"
                 "A=M     //A=LCL+i       \n"
                 "M=D     //*(LCL+i)=*SP  \n",

    "pop argument": "D=A     //D=i           \n"
                    "                        \n"
                    "@ARG                    \n"
                    "D=M+D   //D=ARG+i       \n"
                    "                        \n"
                    "@save_address           \n"
                    "M=D                     \n"
                    "                        \n"
                    "@SP 				     \n"
                    "M=M-1   // SP--         \n"
                    "A=M					 \n"
                    "D=M	//D = *SP	     \n"
                    "                        \n"
                    "@save_address           \n"
                    "A=M     //A=ARG+i       \n"
                    "M=D     //*(ARG+i)=*SP  \n",

    "pop this": "D=A     //D=i           \n"
                "                        \n"
                "@THIS                   \n"
                "D=M+D   //D=THIS+i      \n"
                "                        \n"
                "@save_address           \n"
                "M=D                     \n"
                "                        \n"
                "@SP 				     \n"
                "M=M-1   // SP--         \n"
                "A=M					 \n"
                "D=M	//D = *SP	     \n"
                "                        \n"
                "@save_address           \n"
                "A=M     //A=THIS+i      \n"
                "M=D     //*(THIS+i)=*SP \n",

    "pop that": "D=A     //D=i           \n"
                "                        \n"
                "@THAT                   \n"
                "D=M+D   //D=THAT+i      \n"
                "                        \n"
                "@save_address           \n"
                "M=D                     \n"
                "                        \n"
                "@SP 				     \n"
                "M=M-1   // SP--         \n"
                "A=M					 \n"
                "D=M	//D = *SP	     \n"
                "                        \n"
                "@save_address           \n"
                "A=M     //A=THAT+i      \n"
                "M=D     //*(THAT+i)=*SP \n",

    "pop temp": "D=A     //D=i           \n"
                "                        \n"
                "@5                      \n"
                "D=A+D   //D=5+i         \n"
                "                        \n"
                "@save_address           \n"
                "M=D                     \n"
                "                        \n"
                "@SP 				     \n"
                "M=M-1   // SP--         \n"
                "A=M					 \n"
                "D=M	//D = *SP	     \n"
                "                        \n"
                "@save_address           \n"
                "A=M     //A=5+i         \n"
                "M=D     //*(5+i)=*SP    \n",

    "pop pointer": "D=A     //D=0/1     \n"
                   "@save_pointer       \n"
                   "M=D                 \n"
                   "                    \n"
                   "@SP                 \n"
                   "M=M-1               \n"
                   "A=M                 \n"
                   "D=M                 \n"
                   "@save_value         \n"
                   "M=D                 \n"
                   "                    \n"
                   "@save_pointer       \n"
                   "D=M                 \n"
                   "@IF_THIS*XXX*       \n"
                   "D;JEQ               \n"
                   "                    \n"
                   "@save_value         \n"
                   "D=M                 \n"
                   "@THAT               \n"
                   "M=D                 \n"
                   "@END*XXX*           \n"
                   "0;JMP               \n"
                   "                    \n"
                   "(IF_THIS*XXX*)      \n"
                   "@save_value         \n"
                   "D=M                 \n"
                   "@THIS               \n"
                   "M=D                 \n"
                   "(END*XXX*)          \n",

    "pop static": "D=A     //D=foo.i           \n"
                  "@save_address               \n"
                  "M=D                         \n"
                  "                            \n"
                  "@SP 				           \n"
                  "M=M-1   //SP--              \n"
                  "A=M					       \n"
                  "D=M		//D = *SP	       \n"
                  "                            \n"
                  "@save_address               \n"
                  "A=M     //A=static(i)       \n"
                  "M=D     //*(static(i))=*SP  \n"
}


def clean_line(line):
    """
    clean the line from spaces, tabs, and comments
    :param line: string of line
    :return: string of clean line
    """
    line = line.replace("\t", "")
    line = line.replace("\n", "")
    index_comment = line.find("//")
    print("index of //: ", index_comment)  # todo delete
    if index_comment != -1:  # found comment
        if index_comment == 0:  # all line is just a comment
            line = ""
        else:
            line = line[:index_comment]
    print("clean line: ", line)  # todo delete
    return line


def translate_push_command(segment, index, asm_file, vm_file_name, label_counter):
    if segment == "static":
        asm_file.write("@" + vm_file_name + f".{index}\n")
    else:
        asm_file.write(f"@{index}\n")
    if "*XXX*" in HACK_COMMANDS_TRANSLATION["push " + segment]:  # command has labels in the code (just pointer)
        translation = HACK_COMMANDS_TRANSLATION["push " + segment].replace("*XXX*", str(label_counter))
    else:
        translation = HACK_COMMANDS_TRANSLATION["push " + segment]
    asm_file.write(translation)


def translate_pop_command(segment, index, asm_file, vm_file_name, label_counter):
    if segment == "static":
        asm_file.write("@" + vm_file_name + f".{index}\n")
    else:
        asm_file.write(f"@{index}\n")
    if "*XXX*" in HACK_COMMANDS_TRANSLATION["pop " + segment]:  # command has labels in the code (just pointer)
        translation = HACK_COMMANDS_TRANSLATION["pop " + segment].replace("*XXX*", str(label_counter))
    else:
        translation = HACK_COMMANDS_TRANSLATION["pop " + segment]
    asm_file.write(translation)


def translate_file(lines_list, vm_file_name, asm_file):
    """
    parse a line and use other functions to translate to Hack assembly
    :param lines_list: list of all the lines in a given file
    :param vm_file_name: name of the file
    :param asm_file: the output file to write the translation into
    :return: none
    """
    label_counter = 0
    for line in lines_list:
        print("********************\nline: ", line)  # todo delete
        curr_line = clean_line(line)
        if curr_line == "":
            continue
        asm_file.write("\n// ------ " + curr_line + " ------\n")  # write the original vm command to be translated
        command_list = curr_line.split()
        if len(command_list) == 1:  # only one word in line == Arithmetic/Logical command
            if "*XXX*" in HACK_COMMANDS_TRANSLATION[command_list[0]]:  # command has labels in the code
                translation = HACK_COMMANDS_TRANSLATION[command_list[0]].replace("*XXX*", str(label_counter))
            else:  # command doesnt have labels in the code
                translation = HACK_COMMANDS_TRANSLATION[command_list[0]]
            asm_file.write(translation)
        else:  # Memory command
            print("command_list: ", command_list)
            if command_list[0] == "push":
                translate_push_command(command_list[1], command_list[2], asm_file, vm_file_name, label_counter)
            elif command_list[0] == "pop":
                translate_pop_command(command_list[1], command_list[2], asm_file, vm_file_name, label_counter)
        label_counter += 1


def main():
    # ------------- find vm files to translate ----------------
    arg_string = os.path.abspath(sys.argv[1])
    if not os.path.exists(arg_string):
        print("USAGE: file not found")
        sys.exit(1)
    vm_files_list = []
    name = ""
    if os.path.isdir(arg_string):  # if argument is directory
        for file in os.listdir(arg_string):
            #  print("file found: ", file)
            if file.endswith(".vm"):
                if os.name == 'nt':  # if on windows
                    vm_files_list.append(arg_string + '\\' + file)
                    name = arg_string.split()[0] + '\\' + ntpath.basename(arg_string) + ".asm"  # output file address
                else:  # if on linux
                    vm_files_list.append(arg_string + '/' + file)
                    name = arg_string.split()[0] + '/' + ntpath.basename(arg_string) + ".asm"  # output file address
    else:  # argument is file
        if not sys.argv[1].endswith('.vm'):
            print("USAGE: unsupported file type")
            sys.exit(1)
        else:  # if argument is an vm file
            vm_files_list.append(arg_string)
        name = arg_string.split(".vm")[0] + ".asm"

    asm_file = open(name, "w")  # output file

    # ------------- translate each vm file -------------------
    for vm_file_address in vm_files_list:
        vm_file = open(vm_file_address, "r")
        lines_list = (vm_file.readlines())
        vm_file_name = ntpath.basename(vm_file_address).split(".vm")[0]
        translate_file(lines_list, vm_file_name, asm_file)
        vm_file.close()

    asm_file.close()
    return


if __name__ == '__main__':
    main()
