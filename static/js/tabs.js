const tabHeaders = document.querySelectorAll('.tab-headers li');
const tabContents = document.querySelectorAll('.tab-content');

tabHeaders.forEach(tab => {
  tab.addEventListener('click', () => {
    tabHeaders.forEach(t => t.classList.remove('active'));
    tabContents.forEach(c => c.classList.remove('active'));
    tab.classList.add('active');
    const contentId = tab.dataset.contentId; // Link tabs to content with data attribute
    const content = document.getElementById(contentId); // Access content by ID
    content.classList.add('active');
  });
});


const mainImgs = document.querySelectorAll('.main-img');
const thumbs = document.querySelectorAll('.thumb');

thumbs.forEach(thumb => {
  thumb.addEventListener('click', () => {
    mainImgs.forEach(mainImg => mainImg.classList.remove('main-img-active'));
    const imgId = thumb.dataset.imageId;
    const getMainImg = document.getElementById(`${ imgId }`);
    getMainImg.classList.add('main-img-active');
  });
});
