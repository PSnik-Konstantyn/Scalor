// Referenced Assemblies.
.assembly extern mscorlib
{
  .publickeytoken = (B7 7A 5C 56 19 34 E0 89 ) 
  .ver 4:0:0:0
}

// Our assembly.
.assembly example
{
  .hash algorithm 0x00008004
  .ver 0:0:0:0
}

.module example.exe

// Definition of Program class.
.class private auto ansi beforefieldinit Program
  extends [mscorlib]System.Object
{
    .method private hidebysig static void Main(string[] args) cil managed
    {
    .locals (
       [0]  float32 n10     )
   .entrypoint
   //.maxstack  8
   ldloca    n10
   ldc.r4    1.0
   stind.r4
   ldloca    n10
   ldloc    n10
   ldc.i4    2
   conv.r4
   ldc.i4    2
   conv.r8
   call   float64 [mscorlib]System.Math::Pow(float64, float64)
   add
   stind.r4
   ldloc    n10
   call void [mscorlib]System.Console::WriteLine(float32)
	ret    
}
}