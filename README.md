# Boxblur com MPI

Comandos para executar o benchmark:

```bash
make benchmark
```

Para visualizar um exemplo de saída:

```bash
make show
```

# Tamanho do kernel vs. imagem resultante

Quanto maior o kernel do algoritmo de blur, mais forte é 
o blur.

![Comparação visual](comparacao-visual.png)
# Resultados do benchmark

Rodamos com diferentes tamanhos de Kernel. O tamanho do kernel influencia diretamente no tempo de processamento. Abaixo estão os resultados obtidos:



## Kernel 3x3
### speedup_kernel_3
![Speedup Kernel 3x3](results/speedup_kernel_3.png)
### tempo_kernel_3
![Tempo Kernel 3x3](results/tempo_kernel_3.png)

## Kernel 15x15
### speedup_kernel_15
![Speedup Kernel 15x15](results/speedup_kernel_15.png)
### tempo_kernel_15
![Tempo Kernel 15x15](results/tempo_kernel_15.png)

## Kernel 21x21
### speedup_kernel_21
![Speedup Kernel 21x21](results/speedup_kernel_21.png)
### tempo_kernel_21
![Tempo Kernel 21x21](results/tempo_kernel_21.png)


# Diferença de tempo de cálculo vs. tempo total

Devido ao tempo de execução própria do Python é notável que o tempo total de execução não varia tanto quanto o tempo de cálculo puro do algoritmo. Ele é composto principalmente pelo tempo de leitura de imagens, carregamento de bibliotecas e escrita de arquivos.

Portanto, o que o resultado apresenta é que mesmo que haja um speedup considerável no tempo de cálculo, o tempo total de execução não é tão impactado. Exceto quando o tempo de cálculo é muito maior que o tempo fixo de execução do Python, como no caso do kernel 21x21 com imagens maiores.

## Saída
```
==================== KERNEL SIZE: 3 ====================

[Img 1024x1024] Serial:
  Run 1: Cálculo=0.025s | Total=1.14s
[Img 1024x1024] MPI n=2:
  Run 1: Cálculo=0.013s | Total=1.08s
[Img 1024x1024] MPI n=4:
  Run 1: Cálculo=0.010s | Total=1.21s
[Img 1024x1024] MPI n=8:
  Run 1: Cálculo=0.013s | Total=1.67s


[Img 2048x2048] Serial:
  Run 1: Cálculo=0.091s | Total=1.10s
[Img 2048x2048] MPI n=2:
  Run 1: Cálculo=0.059s | Total=1.24s
[Img 2048x2048] MPI n=4:
  Run 1: Cálculo=0.037s | Total=1.27s
[Img 2048x2048] MPI n=8:
  Run 1: Cálculo=0.033s | Total=1.72s


[Img 4096x4096] Serial:
  Run 1: Cálculo=0.378s | Total=1.39s
[Img 4096x4096] MPI n=2:
  Run 1: Cálculo=0.233s | Total=1.45s
[Img 4096x4096] MPI n=4:
  Run 1: Cálculo=0.147s | Total=1.36s
[Img 4096x4096] MPI n=8:
  Run 1: Cálculo=0.092s | Total=1.62s


==================== KERNEL SIZE: 15 ====================

[Img 1024x1024] Serial:
  Run 1: Cálculo=0.266s | Total=1.23s
[Img 1024x1024] MPI n=2:
  Run 1: Cálculo=0.146s | Total=1.43s
[Img 1024x1024] MPI n=4:
  Run 1: Cálculo=0.140s | Total=1.64s
[Img 1024x1024] MPI n=8:
  Run 1: Cálculo=0.073s | Total=1.78s

[Img 2048x2048] Serial:
  Run 1: Cálculo=1.128s | Total=2.26s
[Img 2048x2048] MPI n=2:
  Run 1: Cálculo=0.584s | Total=1.76s
[Img 2048x2048] MPI n=4:
  Run 1: Cálculo=0.336s | Total=1.64s
[Img 2048x2048] MPI n=8:
  Run 1: Cálculo=0.222s | Total=1.94s

[Img 4096x4096] Serial:
  Run 1: Cálculo=4.270s | Total=5.44s
[Img 4096x4096] MPI n=2:
  Run 1: Cálculo=2.433s | Total=3.76s
[Img 4096x4096] MPI n=4:
  Run 1: Cálculo=1.305s | Total=2.63s
[Img 4096x4096] MPI n=8:
  Run 1: Cálculo=0.968s | Total=2.89s

==================== KERNEL SIZE: 21 ====================

[Img 1024x1024] Serial:
  Run 1: Cálculo=0.495s | Total=1.57s
[Img 1024x1024] MPI n=2:
  Run 1: Cálculo=0.278s | Total=1.44s
[Img 1024x1024] MPI n=4:
  Run 1: Cálculo=0.176s | Total=1.50s
[Img 1024x1024] MPI n=8:
  Run 1: Cálculo=0.114s | Total=1.75s

[Img 2048x2048] Serial:
  Run 1: Cálculo=1.853s | Total=2.80s
[Img 2048x2048] MPI n=2:
  Run 1: Cálculo=1.112s | Total=2.30s
[Img 2048x2048] MPI n=4:
  Run 1: Cálculo=0.652s | Total=2.04s
[Img 2048x2048] MPI n=8:
  Run 1: Cálculo=0.407s | Total=2.10s

[Img 4096x4096] Serial:
  Run 1: Cálculo=7.634s | Total=8.62s
[Img 4096x4096] MPI n=2:
  Run 1: Cálculo=4.525s | Total=5.90s
[Img 4096x4096] MPI n=4:
  Run 1: Cálculo=2.519s | Total=3.81s
[Img 4096x4096] MPI n=8:
  Run 1: Cálculo=1.635s | Total=3.38s
```