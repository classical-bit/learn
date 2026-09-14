# Quantization Fundamentals: How LLMs Run Efficiently with Low Memory
Understanding how model quantization (reducing memory and computational cost) works, why it is critical for LLM inference (the process an LLM uses to generate output in real-time), and how high-precision numbers are mapped to low-bit integers without ruining performance.

1. The Memory Problem
A model with 1 billion parameters stored in standard 32-bit floating-point format (4 bytes per parameter) takes 4GB of VRAM just to load weights.
For models with hundreds of billions of parameters, hosting becomes extra difficult and expensive on modern GPUs without memory optimization. While most base models are trained with 16-bit precision (FP16/BF16) to ensure high-quality calculations, running inference at scale still strains memory.

2. Float vs. Integer Efficiency
Hardware like CPUs and GPUs process integer calculations far more efficiently than floating-point calculations:

 - Floating-Point Arithmetic: Numbers are represented via exponents and mantissas. Operations like addition require aligning exponents, adding mantissas, and normalizing results, taking roughly 3 to 4 CPU cycles.
 - Integer Arithmetic: Drastically reduces memory usage, improves processing speed, and increases energy efficiency on edge devices like smartphones.

3. When Do We Quantize?
 - Post-Training Quantization (PTQ): Shrinks numbers after the model is completely built. It's fast, cheap and widely used.
 - Quantization-Aware Training (QAT): Teaches the model to adapt to low-bit integers during training. Takes more compute time but yields higher accuracy at very low-bit widths.

Note: We shrink static model weights in advance, but dynamic memory (like the KV Cache - the short-term memory during a chat session) is shrunken on the fly during inference.

4. The Math Behind the Squeeze
Quantization turns continuous floating-point numbers (like 3.14159 or -0.82) into discrete integers (like 12 or -4). Because standard integers only have a fixed range (i.e., an 8-bit integer goes from -128 to 127 or 0 to 255), we need a rule to squeeze the float range into that integer range.
The formula connecting a floating-point number (x) to its quantized integer (q) is:

q = round(x / S) + Z

Where:
- S (Scale): A positive float scaling the dynamic range down to the integer range.
- Z (Zero-point): An integer mapping directly to the floating-point value 0.0, ensuring that zero can be represented without quantization error.

During heavy matrix multiplication, operations run fast using low-bit integers. Once calculations are complete, the intermediate accumulated values are scaled back into the floating-point range at the very end to pass to the next layer.
To map back (Dequantization):

x' = S * (q - Z)

This breakdown is based on the insights shared by Arpit Bhayani. Definitely worth watching for a deeper dive into inference engineering! [(Link to the full explanation](https://www.youtube.com/watch?v=FZQpsLfr4xY))
