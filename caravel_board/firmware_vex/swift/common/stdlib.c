int  *memset(void *b, int c, int len)
{
  unsigned char *p = b;
  while(len > 0)
    {
      *p = c;
      p++;
      len--;
    }
  return(b);
}

void memcpy(void *dest, void *src, int n)
{
   // Typecast src and dest addresses to (char *)
   char *csrc = (char *)src;
   char *cdest = (char *)dest;

   // Copy contents of src[] to dest[]
   for (int i=0; i<n; i++)
       cdest[i] = csrc[i];
}

int memcmp (const char * str1, const char * str2, int count)
{
  register const unsigned char *s1 = (const unsigned char*)str1;
  register const unsigned char *s2 = (const unsigned char*)str2;
  while (count-- > 0)
    {
      if (*s1++ != *s2++)
          return s1[-1] < s2[-1] ? -1 : 1;
    }
  return 0;
}

int strlen(const char *str)
{
        const char *s;
        for (s = str; *s; ++s);
        return (s - str);
}