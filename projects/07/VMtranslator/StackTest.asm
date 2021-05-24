
// push constant 17
@17
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// push constant 17
@17
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// eq
@SP				        
M=M-1	// SP--		    
A=M						
D=M	// D=*SP			
                         
@SP						
M=M-1	// SP--		    
A=M						
D=D-M	        	    
                         
@IF_EQUAL			    
D;JEQ				    
@SP		// if not equal	
A=M						
M=0		// *SP=false	
@GOTO_END			    
0;JMP				    
                         
(IF_EQUAL)	// if equal 
@SP						
A=M						
M=1		// *SP=true		
                         
(GOTO_END)				
@SP		// SP++			
M=M+1					

// push constant 17
@17
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// push constant 16
@16
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// eq
@SP				        
M=M-1	// SP--		    
A=M						
D=M	// D=*SP			
                         
@SP						
M=M-1	// SP--		    
A=M						
D=D-M	        	    
                         
@IF_EQUAL			    
D;JEQ				    
@SP		// if not equal	
A=M						
M=0		// *SP=false	
@GOTO_END			    
0;JMP				    
                         
(IF_EQUAL)	// if equal 
@SP						
A=M						
M=1		// *SP=true		
                         
(GOTO_END)				
@SP		// SP++			
M=M+1					

// push constant 16
@16
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// push constant 17
@17
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// eq
@SP				        
M=M-1	// SP--		    
A=M						
D=M	// D=*SP			
                         
@SP						
M=M-1	// SP--		    
A=M						
D=D-M	        	    
                         
@IF_EQUAL			    
D;JEQ				    
@SP		// if not equal	
A=M						
M=0		// *SP=false	
@GOTO_END			    
0;JMP				    
                         
(IF_EQUAL)	// if equal 
@SP						
A=M						
M=1		// *SP=true		
                         
(GOTO_END)				
@SP		// SP++			
M=M+1					

// push constant 892
@892
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// push constant 891
@891
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// lt
@SP						
M=M-1	// SP--			
A=M						
D=M		// D=*SP		
                         
@SP						
M=M-1	// SP--			
A=M						
D=D-M					
                         
@IF_GREATER				
D;JGT					
@SP		//if not greater
A=M						
M=0		// *SP=false	
@GOTO_END				
0;JMP					
                         
(IF_GREATER)			    
@SP						
A=M						
M=1		// *SP=true		
                         
(GOTO_END)				
@SP		// SP++			
M=M+1					

// push constant 891
@891
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// push constant 892
@892
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// lt
@SP						
M=M-1	// SP--			
A=M						
D=M		// D=*SP		
                         
@SP						
M=M-1	// SP--			
A=M						
D=D-M					
                         
@IF_GREATER				
D;JGT					
@SP		//if not greater
A=M						
M=0		// *SP=false	
@GOTO_END				
0;JMP					
                         
(IF_GREATER)			    
@SP						
A=M						
M=1		// *SP=true		
                         
(GOTO_END)				
@SP		// SP++			
M=M+1					

// push constant 891
@891
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// push constant 891
@891
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// lt
@SP						
M=M-1	// SP--			
A=M						
D=M		// D=*SP		
                         
@SP						
M=M-1	// SP--			
A=M						
D=D-M					
                         
@IF_GREATER				
D;JGT					
@SP		//if not greater
A=M						
M=0		// *SP=false	
@GOTO_END				
0;JMP					
                         
(IF_GREATER)			    
@SP						
A=M						
M=1		// *SP=true		
                         
(GOTO_END)				
@SP		// SP++			
M=M+1					

// push constant 32767
@32767
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// push constant 32766
@32766
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// gt
@SP						
M=M-1	// SP--			
A=M						
D=M		// D=*SP		
                         
@SP						
M=M-1	// SP--			
A=M						
D=D-M					
                         
@IF_GREATER				
D;JLT					
@SP		//if not greater
A=M						
M=0		// *SP=false	
@GOTO_END				
0;JMP					
                         
(IF_GREATER)			    
@SP						
A=M						
M=1		// *SP=true		
                         
(GOTO_END)				
@SP		// SP++			
M=M+1					

// push constant 32766
@32766
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// push constant 32767
@32767
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// gt
@SP						
M=M-1	// SP--			
A=M						
D=M		// D=*SP		
                         
@SP						
M=M-1	// SP--			
A=M						
D=D-M					
                         
@IF_GREATER				
D;JLT					
@SP		//if not greater
A=M						
M=0		// *SP=false	
@GOTO_END				
0;JMP					
                         
(IF_GREATER)			    
@SP						
A=M						
M=1		// *SP=true		
                         
(GOTO_END)				
@SP		// SP++			
M=M+1					

// push constant 32766
@32766
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// push constant 32766
@32766
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// gt
@SP						
M=M-1	// SP--			
A=M						
D=M		// D=*SP		
                         
@SP						
M=M-1	// SP--			
A=M						
D=D-M					
                         
@IF_GREATER				
D;JLT					
@SP		//if not greater
A=M						
M=0		// *SP=false	
@GOTO_END				
0;JMP					
                         
(IF_GREATER)			    
@SP						
A=M						
M=1		// *SP=true		
                         
(GOTO_END)				
@SP		// SP++			
M=M+1					

// push constant 57
@57
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// push constant 31
@31
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// push constant 53
@53
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// add
@SP    // D=*SP    
M=M-1	// SP--     
A=M                
D=M                
                   
@SP                
M=M-1   // SP--    
A=M                
M=D+M   // *SP=D+M 
                   
@SP    // SP++     
M=M+1              

// push constant 112
@112
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// sub
@SP	// D=*SP        
M=M-1	// SP--     
A=M                 
D=-M                
                    
@SP                 
M=M-1	// SP--     
A=M                 
M=D+M	// *SP=D+M  
                    
@SP		// SP++     
M=M+1               

// neg
@SP		// D=*SP    
M=M-1	// SP--		
A=M					
M=-M				
                    
@SP					
M=M+1	// SP++		

// and
@SP						
M=M-1	// SP--			
A=M						
D=M		// D=*SP		
                        
@SP						
M=M-1	// SP--			
A=M						
M=D&M	//M = D and M	
                        
@SP		// SP++			
M=M+1					

// push constant 82
@82
D=A	//D = index   	
                       
@SP					
A=M					
M=D	//*SP = i		
                       
@SP	// SP++		    
M=M+1				    

// or
@SP						
M=M-1	// SP--			
A=M						
D=M		// D=*SP		
                         
@SP						
M=M-1	// SP--			
A=M						
M=D|M	// M = D or M	
                         
@SP		// SP++			
M=M+1					

// not
@SP						
M=M-1	// SP--			
A=M						
M=!M	// *SP= not M	
                        
@SP	// SP++		    	
M=M+1					
