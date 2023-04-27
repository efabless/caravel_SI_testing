/**
 \file
*/
#ifndef USER_ADDR_SPACE_C_HEADER_FILE
#define USER_ADDR_SPACE_C_HEADER_FILE
/**
 * Write double word (4 bytes) at user address space 32 bit register
 *  
 * @param data double world data to write
 * @param offset the offset of the register to write. Origin at the user project address
 * 
 * \note 
 * Since offset is a doubleword (4 bytes) and address space represent bytes, offset = address /4
 * \n For example if project caravel space are 26 address bit offset = wb_addr_i[25:0]/4
 * 
 * <table>
    <caption id="multi_row">double world memory (4 bytes offset)</caption>
    <tr><th>address<th>offset <th>byte0<th>byte1<th>byte2<th>byte3
    <tr><td>0x0<td>0<td style="background-color:#FED64E">0<td style="background-color:#FED64E">1<td style="background-color:#FED64E">2<td style="background-color:#FED64E">3
    <tr><td>0x4<td>1<td style="background-color:#EDBB99">4<td style="background-color:#EDBB99">5<td style="background-color:#EDBB99">6<td style="background-color:#EDBB99">7
    <tr><td>0x8<td>2<td style="background-color:#FED64E">8<td style="background-color:#FED64E" >9<td style="background-color:#FED64E">10<td style="background-color:#FED64E">11
    <tr><td>0xC<td>3<td style="background-color:#EDBB99">12<td style="background-color:#EDBB99">13<td style="background-color:#EDBB99">14<td style="background-color:#EDBB99">15   </table>

 */
void write_user_double_word(unsigned int data,int offset){
    *(((unsigned int *) USER_SPACE_ADDR)+offset) = data;

}
/**
 * Read double word (4 bytes) at user address space 32 bit register
 *  
 * @param offset the offset of the register to write. Origin at the user project address
 * 
 * \note 
 * Since offset is a doubleword (4 bytes) and address space represent bytes, offset = address /4
 * \n For example if project caravel space are 26 address bit offset = wb_addr_i[25:0]/4
 * 
 *  <table>
    <caption id="multi_row">double world memory (4 bytes offset)</caption>
    <tr><th>address<th>offset <th>byte0<th>byte1<th>byte2<th>byte3
    <tr><td>0x0<td>0<td style="background-color:#FED64E">0<td style="background-color:#FED64E">1<td style="background-color:#FED64E">2<td style="background-color:#FED64E">3
    <tr><td>0x4<td>1<td style="background-color:#EDBB99">4<td style="background-color:#EDBB99">5<td style="background-color:#EDBB99">6<td style="background-color:#EDBB99">7
    <tr><td>0x8<td>2<td style="background-color:#FED64E">8<td style="background-color:#FED64E" >9<td style="background-color:#FED64E">10<td style="background-color:#FED64E">11
    <tr><td>0xC<td>3<td style="background-color:#EDBB99">12<td style="background-color:#EDBB99">13<td style="background-color:#EDBB99">14<td style="background-color:#EDBB99">15   </table>

 */
unsigned int read_user_double_word(int offset){
    return *(((unsigned int *) USER_SPACE_ADDR)+offset);
}
/**
 * Write word (2 bytes) at user address space 32 bit register
 *  
 * @param data  world data to write
 * @param offset the offset of the register to write. Origin at the user project address
 * @param is_first_word the offset of the register to write. Origin at the user project address
 * 
 * \note 
 * Since offset is a doubleword (4 bytes) and address space represent bytes, offset = address /4
 * \n For example if project caravel space are 26 address bit offset = wb_addr_i[25:0]/4
 * 
 *  <table>
    <caption id="multi_row"> world memory (2byte offset)</caption>
    <tr><th>is first word<th>-<th> 1<th> 1 <th>0<th>0
    <tr><th>address<th>offset <th>byte0<th>byte1<th>byte2<th>byte3
    <tr><td>0x0<td>0<td style="background-color:#FEF5E7">0<td style="background-color:#FEF5E7">1<td style="background-color:#FED64E">2<td style="background-color:#FED64E">3
    <tr><td>0x4<td>1<td style="background-color:#FAD7A0">4<td style="background-color:#FAD7A0">5<td style="background-color:#EDBB99">6<td style="background-color:#EDBB99">7
    <tr><td>0x8<td>2<td style="background-color:#FEF5E7">8<td style="background-color:#FEF5E7" >9<td style="background-color:#FED64E">10<td style="background-color:#FED64E">11
    <tr><td>0xC<td>3<td style="background-color:#FAD7A0">12<td style="background-color:#FAD7A0">13<td style="background-color:#EDBB99">14<td style="background-color:#EDBB99">15   </table>

 */
void write_user_word(unsigned short data,unsigned int offset,bool is_first_word){
    unsigned int half_word_offset = offset *2 + is_first_word;
    *(((unsigned int *) USER_SPACE_ADDR)+half_word_offset) = data;
    
}
/**
 * Read word (2 bytes) at user address space 32 bit register
 *  
 * @param offset the offset of the register to write. Origin at the user project address
 * @param is_first_word the offset of the register to write. Origin at the user project address
 * 
 * \note 
 * Since offset is a doubleword (4 bytes) and address space represent bytes, offset = address /4
 * \n For example if project caravel space are 26 address bit offset = wb_addr_i[25:0]/4
 * 
 *  <table>
    <caption id="multi_row"> world memory (2byte offset)</caption>
    <tr><th>is first word<th>-<th> 1<th> 1 <th>0<th>0
    <tr><th>address<th>offset <th>byte0<th>byte1<th>byte2<th>byte3
    <tr><td>0x0<td>0<td style="background-color:#FEF5E7">0<td style="background-color:#FEF5E7">1<td style="background-color:#FED64E">2<td style="background-color:#FED64E">3
    <tr><td>0x4<td>1<td style="background-color:#FAD7A0">4<td style="background-color:#FAD7A0">5<td style="background-color:#EDBB99">6<td style="background-color:#EDBB99">7
    <tr><td>0x8<td>2<td style="background-color:#FEF5E7">8<td style="background-color:#FEF5E7" >9<td style="background-color:#FED64E">10<td style="background-color:#FED64E">11
    <tr><td>0xC<td>3<td style="background-color:#FAD7A0">12<td style="background-color:#FAD7A0">13<td style="background-color:#EDBB99">14<td style="background-color:#EDBB99">15   </table>

 */
unsigned short read_user_word(unsigned int offset,bool is_first_word){
    unsigned int half_word_offset = offset *2 + is_first_word;
    return *(((unsigned int *) USER_SPACE_ADDR)+half_word_offset);
}
/**
 * Write byte  at user address space 32 bit register
 *  
 * @param data byte data to write
 * @param offset the offset of the register to write. Origin at the user project address
 * @param byte_num number of the in the 4 bytes register (32 bits)
 * 
 * \note 
 * Since offset is a doubleword (4 bytes) and address space represent bytes, offset = address /4
 * \n For example if project caravel space are 26 address bit offset = wb_addr_i[25:0]/4
 * 
 *  <table>
    <caption id="multi_row"> world memory (2byte offset)</caption>
    <tr><th >byte_num<th>-<th> 0 <th >1<th >2<th >3
    <tr><th>address<th>offset <th>byte0<th>byte1<th>byte2<th>byte3
    <tr><td>0x0<td>0<td style="background-color:#FEF5E7">0<td style="background-color:#FAD7A0">1<td style="background-color:#FED64E">2<td style="background-color:#EDBB99">3
    <tr><td>0x4<td>1<td style="background-color:#FED64E">4<td style="background-color:#EDBB99">5<td style="background-color:#FEF5E7">6<td style="background-color:#FAD7A0">7
    <tr><td>0x8<td>2<td style="background-color:#FEF5E7">8<td style="background-color:#FAD7A0" >9<td style="background-color:#FED64E">10<td style="background-color:#EDBB99">11
    <tr><td>0xC<td>3<td style="background-color:#FED64E">12<td style="background-color:#EDBB99">13<td style="background-color:#FEF5E7">14<td style="background-color:#FAD7A0">15   </table>

 */
void write_user_byte(unsigned char data,unsigned int offset,unsigned char byte_num){
    if (byte_num > 3) 
        byte_num =0; 
    unsigned int byte_offset = offset *4 + byte_num;
    *(((unsigned int *) USER_SPACE_ADDR)+byte_offset) = data;
}
/**
 * Read byte  at user address space 32 bit register
 *  
 * @param offset the offset of the register to write. Origin at the user project address
 * @param byte_num number of the in the 4 bytes register (32 bits)
 * 
 * \note 
 * Since offset is a doubleword (4 bytes) and address space represent bytes, offset = address /4
 * \n For example if project caravel space are 26 address bit offset = wb_addr_i[25:0]/4
 * 
 *  <table>
    <caption id="multi_row"> world memory (2byte offset)</caption>
    <tr><th >byte_num<th>-<th> 0 <th >1<th >2<th >3
    <tr><th>address<th>offset <th>byte0<th>byte1<th>byte2<th>byte3
    <tr><td>0x0<td>0<td style="background-color:#FEF5E7">0<td style="background-color:#FAD7A0">1<td style="background-color:#FED64E">2<td style="background-color:#EDBB99">3
    <tr><td>0x4<td>1<td style="background-color:#FED64E">4<td style="background-color:#EDBB99">5<td style="background-color:#FEF5E7">6<td style="background-color:#FAD7A0">7
    <tr><td>0x8<td>2<td style="background-color:#FEF5E7">8<td style="background-color:#FAD7A0" >9<td style="background-color:#FED64E">10<td style="background-color:#EDBB99">11
    <tr><td>0xC<td>3<td style="background-color:#FED64E">12<td style="background-color:#EDBB99">13<td style="background-color:#FEF5E7">14<td style="background-color:#FAD7A0">15   </table>

 */
unsigned char read_user_byte( unsigned int offset,unsigned char byte_num){
    if (byte_num > 3) 
        byte_num =0; 
    unsigned int byte_offset = offset *4 + byte_num;
    return *(((unsigned int *) USER_SPACE_ADDR)+byte_offset);
}

#endif // USER_ADDR_SPACE_C_HEADER_FILE
