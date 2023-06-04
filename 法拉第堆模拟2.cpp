#include <iomanip>
#include <iostream>
#include <random>
#include <vector>

// 模拟系统.
struct Sim {
  // 初始堆数.
  int n0;
  // 当前堆数.
  int n;
  // 迭代速率.
  double rate;
  // 堆的左侧、右侧尺度.
  std::vector<double> l, r;
  // 迭代过程中使用的临时数组.
  std::vector<double> lt, rt;
  // 堆数持续时间的计数器.
  std::vector<unsigned> counter;

  // 初始化变量.
  Sim(int n, double rate)
      : n0(n), n(n), rate(rate), l(n), r(n), lt(n), rt(n), counter(n + 1) {}

  // 重置模拟状态.
  void Reset() {
    n = n0;

    std::random_device seed;
    std::mt19937 gen(seed());                       // 随机数生成器.
    std::uniform_real_distribution<> dist(0., 1.);  // 0-1 均匀分布.

    double l_sum = 0., r_sum = 0.;
    for (int i = 0; i < n; ++i) {
      l_sum += l[i] = dist(gen);  // 堆尺度为随机数.
      r_sum += r[i] = dist(gen);
    }
    for (int i = 0; i < n; ++i) {
      l[i] *= n / l_sum;  // 将平均尺度调整为 1.
      r[i] *= n / r_sum;
    }
  }

  // 计算堆尺度改变量.
  __attribute__((always_inline)) constexpr double f(double u, double v) const {
    return rate * v * (u - v) / (u * u + v * v) / (u + v);
  }

  // 模拟迭代.
  void Step() {
    // 计算新的堆尺度, 保存到 lt、rt 数组.
    lt[0] = l[0] + f(l[0], r[0]);  // 最左堆.
    for (int i = 0; i < n - 1; ++i) {
      // 中间的堆受左右相邻堆的影响.
      rt[i] = r[i] + f(r[i], l[i]) - f(r[i + 1], l[i + 1]);
      lt[i + 1] = l[i + 1] + f(l[i + 1], r[i + 1]) - f(l[i], r[i]);
    }
    rt[n - 1] = r[n - 1] + f(r[n - 1], l[n - 1]);  // 最右堆.

    // 判断堆是否发生合并, 并将剩下的堆写回 l、r 数组.
    int nt = 0;  // nt 表示新的堆数.
    l[0] = lt[0];
    r[0] = 0.;

    // i 表示堆之间的谷, 共 n-1 个谷.
    for (int i = 0; i < n - 1; ++i) {
      r[nt] += rt[i];  // 将谷左侧的堆尺度写回 r.

      // 判断这个谷是否仍然存在, 考察两侧尺度是否为正.
      if (rt[i] > 0. && lt[i + 1] > 0.) {
        // 谷仍然存在的情况. 标记新的堆.
        ++nt;
        l[nt] = r[nt] = 0.;
      }

      l[nt] += lt[i + 1];  // 将谷右侧的堆尺度写回 l.
    }

    r[nt] += rt[n - 1];
    n = nt + 1;  // 写回新的堆数.
  }

  // 持续迭代并计数, 直到堆数小于 3.
  void Run() {
    Reset();
    while (n >= 3) {
      ++counter[n];
      Step();
    }
  }
};

// 使用命令行指定参数, 分别为初始堆数、迭代速率、重复次数.
int main(int argc, char **argv) {
  if (argc != 4) {
    std::cerr << "Usage: " << argv[0] << " <n> <rate> <repeats>\n";
    return 1;
  }
  int n = std::stoi(argv[1]);
  double rate = std::stod(argv[2]);
  int repeats = std::stoi(argv[3]);

  Sim sim(n, rate);
  for (int t = 1; t <= repeats; ++t) {
    sim.Run();
    if (t % 100 == 0) {
      std::cerr << std::setw(3) << (t * 100 / repeats) << "%\n";
    }
  }

  for (int i = 3; i <= n; ++i) {
    std::cout << std::setw(3) << i << ',' << std::setw(10) << sim.counter[i]
              << ".\n";
  }
}
