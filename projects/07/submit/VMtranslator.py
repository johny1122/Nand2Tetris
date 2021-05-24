# project 7
# This VMtranslator write all the translations at the beginning of the file and just call and jump
# to the right translate each line, so good for large vm programs (no code duplication)

import sys
import re
import os
import ntpath

HACK_COMMAND_TRANSLATION = {
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
           "M=M+1              \n"
           "@R14               \n"
           "A=M                \n"
           "0;JMP              \n",

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
           "M=M+1               \n"
           "@R14                \n"
           "A=M                 \n"
           "0;JMP               \n",

    "neg": "@SP		// D=*SP    \n"
           "M=M-1	// SP--		\n"
           "A=M					\n"
           "M=-M				\n"
           "                    \n"
           "@SP					\n"
           "M=M+1	// SP++		\n"
           "@R14                \n"
           "A=M                 \n"
           "0;JMP               \n",

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
          "@IF_EQUAL_EQ  	          \n"
          "D;JEQ				      \n"
          "@SP		// if not equal	  \n"
          "A=M						  \n"
          "M=0		// *SP=false	  \n"
          "@GOTO_END_EQ		          \n"
          "0;JMP				      \n"
          "                           \n"
          "(IF_EQUAL_EQ)// if equal   \n"
          "@SP						  \n"
          "A=M						  \n"
          "M=-1		// *SP=true		  \n"
          "                           \n"
          "(GOTO_END_EQ)			  \n"
          "@SP		// SP++			  \n"
          "M=M+1					  \n"
          "@R14                       \n"
          "A=M                        \n"
          "0;JMP                      \n",

    "gt": "@SP						    		        \n"
          "M=M-1	// SP--			   			        \n"
          "A=M						    		        \n"
          "D=M		// D=*SP (y)	    		        \n"
          "                                             \n"
          "@y									        \n"
          "M=D									        \n"
          "                                             \n"
          "@SP						    		        \n"
          "M=M-1	// SP--			    		        \n"
          "A=M						    		        \n"
          "D=M		// D=*SP (x)	    		        \n"
          "                                             \n"
          "@x									        \n"
          "M=D									        \n"
          "                                             \n"
          "@IF_X_POSITIVE_GT	//x>0			        \n"
          "D;JGT								        \n"
          "@IF_X_NEGATIVE_OR_ZERO_GT	//x<=0	        \n"
          "0;JMP								        \n"
          "                                             \n"
          "                                             \n"
          "(IF_X_POSITIVE_GT)					        \n"
          "@y									        \n"
          "D=M									        \n"
          "                                             \n"
          "@IF_X_AND_Y_POS_GT		//x&y>0		        \n"
          "D;JGT	//y>0						        \n"
          "                                             \n"
          "@IF_TRUE_GT	//x>0 & y<=0			        \n"
          "0;JMP								        \n"
          "                                             \n"
          "(IF_X_AND_Y_POS_GT)					        \n"
          "@x									        \n"
          "D=M									        \n"
          "@y									        \n"
          "D=M-D	//D=y-x						        \n"
          "@IF_FALSE_GT	//y-x>=0 == x<=y		        \n"
          "D;JGE								        \n"
          "@IF_TRUE_GT	//y-x<0 == x>y			        \n"
          "0;JMP								        \n"
          "                                             \n"
          "(IF_X_NEGATIVE_OR_ZERO_GT)			        \n"
          "@y									        \n"
          "D=M                                          \n"
          "@IF_X_AND_Y_ARE_NEG_OR_ZERO_GT	//x&y<=0	\n"
          "D;JLE	//y<=0								\n"
          "                                             \n"
          "@IF_FALSE_GT	//x<=0 & y>0					\n"
          "0;JMP										\n"
          "                                             \n"
          "(IF_X_AND_Y_ARE_NEG_OR_ZERO_GT)				\n"
          "@x											\n"
          "D=M											\n"
          "@y											\n"
          "D=M-D	//D=y-x								\n"
          "@IF_TRUE_GT	//y-x<0 == y<x					\n"
          "D;JLT										\n"
          "@IF_FALSE_GT	//y-x>=0 == y>=x				\n"
          "0;JMP										\n"
          "                                             \n"
          "(IF_TRUE_GT)		//if x>y				    \n"
          "@SP		   									\n"
          "A=M						    				\n"
          "M=-1			// *SP=true						\n"
          "@GOTO_END_GT			    					\n"
          "0;JMP										\n"
          "                                             \n"
          "(IF_FALSE_GT)		//if x<=y		    	\n"
          "@SP		   									\n"
          "A=M						    				\n"
          "M=0				// *SP=false				\n"
          "                                             \n"
          "(GOTO_END_GT)			    			    \n"
          "@SP		// SP++			    				\n"
          "M=M+1					    				\n"
          "@R14                                         \n"
          "A=M                                          \n"
          "0;JMP                                        \n",

    "lt": "@SP						    				\n"
          "M=M-1	// SP--			   					\n"
          "A=M						    				\n"
          "D=M		// D=*SP (y)	    				\n"
          "                                             \n"
          "@y											\n"
          "M=D											\n"
          "                                             \n"
          "@SP						    				\n"
          "M=M-1	// SP--			    				\n"
          "A=M						    				\n"
          "D=M		// D=*SP (x)	    				\n"
          "                                             \n"
          "@x											\n"
          "M=D											\n"
          "                                             \n"
          "@IF_X_POSITIVE_LT	//x>0		    		\n"
          "D;JGT										\n"
          "@IF_X_NEGATIVE_OR_ZERO_LT	//x<=0	    	\n"
          "0;JMP										\n"
          "                                             \n"
          "(IF_X_POSITIVE_LT)				    		\n"
          "@y											\n"
          "D=M											\n"
          "                                             \n"
          "@IF_X_AND_Y_POS_LT		//x&y>0		    	\n"
          "D;JGT	//y>0								\n"
          "                                             \n"
          "@IF_FALSE_LT	//x>0 & y<=0					\n"
          "0;JMP										\n"
          "                                             \n"
          "(IF_X_AND_Y_POS_LT)							\n"
          "@x											\n"
          "D=M											\n"
          "@y											\n"
          "D=M-D	//D=y-x								\n"
          "@IF_TRUE_LT	//y-x>0 == x<y					\n"
          "D;JGT										\n"
          "@IF_FALSE_LT	//y-x<=0 == x>=y				\n"
          "0;JMP										\n"
          "                                             \n"
          "(IF_X_NEGATIVE_OR_ZERO_LT)		    		\n"
          "@y											\n"
          "D=M											\n"
          "@IF_X_AND_Y_ARE_NEG_OR_ZERO_LT	//x&y<=0	\n"
          "D;JLE	//y<=0								\n"
          "                                             \n"
          "@IF_TRUE_LT	//x<=0 & y>0					\n"
          "0;JMP										\n"
          "                                             \n"
          "(IF_X_AND_Y_ARE_NEG_OR_ZERO_LT)				\n"
          "@x											\n"
          "D=M											\n"
          "@y											\n"
          "D=M-D	//D=y-x								\n"
          "@IF_TRUE_LT	//y-x>0 == x<y					\n"
          "D;JGT										\n"
          "@IF_FALSE_LT	//y-x<=0 == x>=y				\n"
          "0;JMP										\n"
          "                                             \n"
          "(IF_TRUE_LT)		//if x<y					\n"
          "@SP		   									\n"
          "A=M						    				\n"
          "M=-1			// *SP=true						\n"
          "@GOTO_END_LT   		    					\n"
          "0;JMP										\n"
          "                                             \n"
          "(IF_FALSE_LT)		//if x>=y		    	\n"
          "@SP		   									\n"
          "A=M						    				\n"
          "M=0				// *SP=false				\n"
          "                                             \n"
          "(GOTO_END_LT)		    	    			\n"
          "@SP		// SP++			    				\n"
          "M=M+1					    				\n"
          "@R14                                         \n"
          "A=M                                          \n"
          "0;JMP                                        \n",

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
           "M=M+1					\n"
           "@R14                    \n"
           "A=M                     \n"
           "0;JMP                   \n",

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
          "M=M+1					\n"
          "@R14                     \n"
          "A=M                      \n"
          "0;JMP                    \n",

    "not": "@SP						\n"
           "M=M-1	// SP--			\n"
           "A=M						\n"
           "M=!M	// *SP= not M	\n"
           "                        \n"
           "@SP	// SP++		    	\n"
           "M=M+1					\n"
           "@R14                    \n"
           "A=M                     \n"
           "0;JMP                   \n",

    # PUSH - Memory commands

    "push_constant": "@SP					 \n"
                     "A=M					 \n"
                     "M=D	//*SP = D		 \n"
                     "                       \n"
                     "@SP	// SP++		     \n"
                     "M=M+1				     \n"
                     "@R14                   \n"
                     "A=M                    \n"
                     "0;JMP                  \n",

    "push_local": "@LCL                 \n"
                  "D=M+D   //D=LCL+i    \n"
                  "A=D                  \n"
                  "D=M     //D=*(LCL+i) \n"
                  "                     \n"
                  "@SP					\n"
                  "A=M					\n"
                  "M=D		//*SP = D	\n"
                  "                     \n"
                  "@SP		// SP++		\n"
                  "M=M+1				\n"
                  "@R14                 \n"
                  "A=M                  \n"
                  "0;JMP                \n",

    "push_argument": "@ARG                \n"
                     "D=M+D   //D=ARG+i   \n"
                     "A=D                 \n"
                     "D=M     //D=*(ARG+i)\n"
                     "                    \n"
                     "@SP                 \n"
                     "A=M                 \n"
                     "M=D    //*SP = D	  \n"
                     "                    \n"
                     "@SP		// SP++	  \n"
                     "M=M+1				  \n"
                     "@R14                \n"
                     "A=M                 \n"
                     "0;JMP               \n",

    "push_this": "@THIS                \n"
                 "D=M+D   //D=THIS+i   \n"
                 "A=D                  \n"
                 "D=M     //D=*(THIS+i)\n"
                 "                     \n"
                 "@SP				   \n"
                 "A=M				   \n"
                 "M=D		//*SP = D  \n"
                 "                     \n"
                 "@SP		// SP++	   \n"
                 "M=M+1				   \n"
                 "@R14                 \n"
                 "A=M                  \n"
                 "0;JMP                \n",

    "push_that": "@THAT                \n"
                 "D=M+D   //D=THAT+i   \n"
                 "A=D                  \n"
                 "D=M     //D=*(THAT+i)\n"
                 "                     \n"
                 "@SP				   \n"
                 "A=M				   \n"
                 "M=D		//*SP = D  \n"
                 "                     \n"
                 "@SP		// SP++	   \n"
                 "M=M+1				   \n"
                 "@R14                 \n"
                 "A=M                  \n"
                 "0;JMP                \n",

    "push_temp": "@5                   \n"
                 "D=A+D   //D=5+i      \n"
                 "A=D                  \n"
                 "D=M     //D=*(5+i)   \n"
                 "                     \n"
                 "@SP				   \n"
                 "A=M				   \n"
                 "M=D		//*SP = D  \n"
                 "                     \n"
                 "@SP		// SP++	   \n"
                 "M=M+1				   \n"
                 "@R14                 \n"
                 "A=M                  \n"
                 "0;JMP                \n",

    "push_pointer": "@IF_THIS_PUSH_POINTER      \n"
                    "D;JEQ                      \n"
                    "                           \n"
                    "@THAT   //if that (1)      \n"
                    "D=M                        \n"
                    "@END_PUSH_POINTER          \n"
                    "0;JMP                      \n"
                    "                           \n"
                    "(IF_THIS_PUSH_POINTER) //(0)\n"
                    "@THIS                      \n"
                    "D=M                        \n"
                    "                           \n"
                    "(END_PUSH_POINTER)         \n"
                    "@SP				        \n"
                    "A=M				        \n"
                    "M=D		//*SP = D       \n"
                    "                           \n"
                    "@SP		// SP++	        \n"
                    "M=M+1				        \n"
                    "@R14                       \n"
                    "A=M                        \n"
                    "0;JMP                      \n",

    "push_static": "@SP					\n"
                   "A=M					\n"
                   "M=D		//*SP = D	\n"
                   "                    \n"
                   "@SP		// SP++		\n"
                   "M=M+1				\n"
                   "@R14                \n"
                   "A=M                 \n"
                   "0;JMP               \n",

    # POP - Memory commands

    "pop_local": "@LCL                    \n"
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
                 "M=D     //*(LCL+i)=*SP  \n"
                 "@R14                    \n"
                 "A=M                     \n"
                 "0;JMP                   \n",

    "pop_argument": "@ARG                    \n"
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
                    "M=D     //*(ARG+i)=*SP  \n"
                    "@R14                    \n"
                    "A=M                     \n"
                    "0;JMP                   \n",

    "pop_this": "@THIS                   \n"
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
                "M=D     //*(THIS+i)=*SP \n"
                "@R14                    \n"
                "A=M                     \n"
                "0;JMP                   \n",

    "pop_that": "@THAT                   \n"
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
                "M=D     //*(THAT+i)=*SP \n"
                "@R14                    \n"
                "A=M                     \n"
                "0;JMP                   \n",

    "pop_temp": "@5                      \n"
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
                "M=D     //*(5+i)=*SP    \n"
                "@R14                    \n"
                "A=M                     \n"
                "0;JMP                   \n",

    "pop_pointer": "@save_pointer       \n"
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
                   "@IF_THIS_POP_POINTER\n"
                   "D;JEQ               \n"
                   "                    \n"
                   "@save_value         \n"
                   "D=M                 \n"
                   "@THAT               \n"
                   "M=D                 \n"
                   "@END_POP_POINTER    \n"
                   "0;JMP               \n"
                   "                    \n"
                   "(IF_THIS_POP_POINTER)\n"
                   "@save_value         \n"
                   "D=M                 \n"
                   "@THIS               \n"
                   "M=D                 \n"
                   "(END_POP_POINTER)   \n"
                   "@R14                \n"
                   "A=M                 \n"
                   "0;JMP               \n",

    "pop_static": "@save_address               \n"
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
                  "@R14                        \n"
                  "A=M                         \n"
                  "0;JMP                       \n"
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
    if index_comment != -1:  # found comment
        if index_comment == 0:  # all line is just a comment
            line = ""
        else:
            line = line[:index_comment]
    return line


def write_functions_at_top(asm_file):
    """
    writes all the translations to the beginning of the output asm file and the jump command
    to jump over all the translations
    :param asm_file: name of the output asm file
    :return: none
    """
    asm_file.write("@JUMP_TO_START      // jump to start\n"
                   "0;JMP\n")
    for function in HACK_COMMAND_TRANSLATION:
        asm_file.write(f"({function})\n")
        asm_file.write(HACK_COMMAND_TRANSLATION[function] + "\n")
    asm_file.write("(JUMP_TO_START)\n")


def translate_push_command(segment, index, asm_file, vm_file_name):
    """
    write a jump to the right push command
    :param segment: type of push command
    :param index: index of the segment in the command
    :param asm_file: the output asm file
    :param vm_file_name: the name of the input vm file
    :return: none
    """
    if segment == "static":  # static had a special beginning
        asm_file.write("@" + vm_file_name + f".{index}\n")
        asm_file.write("D=M     //D=foo.i\n")
    else:
        asm_file.write(f"@{index}\n")
        asm_file.write("D=A	    //D = i\n")
    asm_file.write(f"@push_{segment}\n"
                   "0;JMP\n")


def translate_pop_command(segment, index, asm_file, vm_file_name):
    """
    write a jump to the right pop command
    :param segment: type of pop command
    :param index: index of the segment in the command
    :param asm_file: the output asm file
    :param vm_file_name: the name of the input vm file
    :return: none
    """
    if segment == "static":  # static had a special beginning
        asm_file.write("@" + vm_file_name + f".{index}\n")
    else:
        asm_file.write(f"@{index}\n")
    asm_file.write("D=A\n")
    asm_file.write(f"@pop_{segment}\n"
                   "0;JMP\n")


def translate_file(lines_list, vm_file_name, asm_file):
    """
    parse a line and use other functions to translate to Hack assembly
    :param lines_list: list of all the lines in a given file
    :param vm_file_name: name of the file
    :param asm_file: the output file to write the translation into
    :return: none
    """
    label_counter = 0
    write_functions_at_top(asm_file)
    for line in lines_list:
        curr_line = clean_line(line)
        if curr_line == "":
            continue
        asm_file.write("\n// ------ " + curr_line + " ------\n")  # write the original vm command to be
        # translated
        command_list = curr_line.split()
        asm_file.write(f"@Jump_{label_counter}\n"
                       "D=A\n"
                       "@R14\n"
                       "M=D\n")
        if len(command_list) == 1:  # only one word in line == Arithmetic/Logical command
            asm_file.write(f"@{command_list[0]}\n"
                           "0;JMP\n")

        else:  # Memory command
            if command_list[0] == "push":
                translate_push_command(command_list[1], command_list[2], asm_file, vm_file_name)
            elif command_list[0] == "pop":
                translate_pop_command(command_list[1], command_list[2], asm_file, vm_file_name)
        asm_file.write(f"(Jump_{label_counter})\n")
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
            if file.endswith(".vm"):
                if os.name == 'nt':  # if on windows
                    vm_files_list.append(arg_string + '\\' + file)
                    name = arg_string.split()[0] + '\\' + ntpath.basename(
                        arg_string) + ".asm"  # output file address
                else:  # if on linux
                    vm_files_list.append(arg_string + '/' + file)
                    name = arg_string.split()[0] + '/' + ntpath.basename(
                        arg_string) + ".asm"  # output file address
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
