/*
  首页封面图片轮播：每隔几秒切到下一张，实现淡入淡出。
  图片列表来自 _config.yaml 的 header-slides。
*/

{
  const INTERVAL = 6000;

  const onLoad = () => {
    const slides = [...document.querySelectorAll(".hero-slide")];
    if (slides.length < 2) return;

    // 尊重系统的「减少动态效果」设置，不自动切换
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    let index = 0;
    let timer = null;

    // 页面在后台时暂停，避免切回来时连续跳帧
    const start = () => {
      if (timer) return;
      timer = setInterval(() => {
        slides[index].classList.remove("is-active");
        index = (index + 1) % slides.length;
        slides[index].classList.add("is-active");
      }, INTERVAL);
    };

    const stop = () => {
      clearInterval(timer);
      timer = null;
    };

    start();

    document.addEventListener("visibilitychange", () => {
      if (document.hidden) stop();
      else start();
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onLoad);
  } else {
    onLoad();
  }
}