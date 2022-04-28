let img_search = document.querySelector("img.search");
let input_search = document.querySelector("input.search");

input_search.addEventListener("keypress", (e) => {
    if (e.keyCode === 13) {
        img_search.click();
    }
});

img_search.addEventListener("click", (e) => {
    let input_search = document.querySelector("input.search");
    let input_syno = document.querySelector("input.syno");
    let keyword2 = document.querySelector("div.keyword2");
    let brand2 = document.querySelector("div.brand2");

    let data = JSON.stringify({
        keyword: input_search.value,
        synonym: input_syno.checked,
    });

    fetch("/ml", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: data,
    })
        .then((res) => res.json())
        .then((res_json) => {
            console.log(res_json);

            while (keyword2.firstChild) {
                keyword2.removeChild(keyword2.firstChild);
            }

            while (brand2.firstChild) {
                brand2.removeChild(brand2.firstChild);
            }

            // section1
            s1_num = res_json.section1.s1_1.length;
            for (let i = 0; i < s1_num; i++) {
                let title = document.createElement("div");
                title.classList.add("keyword-title");
                title.innerText = `與 ${res_json.section1.s1_1[i]} 有關的文字/相似度：`;
                keyword2.appendChild(title);

                for (let x = 0; x < res_json.section1.s1_2[i].length; x++) {
                    let ky_answer = document.createElement("div");
                    ky_answer.classList.add("keyword-answer");
                    ky_answer.innerText = `${res_json.section1.s1_2[i][x]}: ${res_json.section1.s1_3[i][x]}`;
                    keyword2.appendChild(ky_answer);
                }
            }

            //section2
            let brand_title = document.createElement("div");
            brand_title.classList.add("brand-title");
            brand_title.innerText = `與 ${input_search.value} 有關的品牌：`;
            brand2.appendChild(brand_title);

            s2_num = res_json.section2.s2_1.length;
            for (let i = 0; i < s2_num; i++) {
                let brand_answer = document.createElement("div");
                brand_answer.classList.add("brand-answer");
                brand_answer.innerText = `${res_json.section2.s2_1[i]}: ${res_json.section2.s2_2[i]}`;
                brand2.appendChild(brand_answer);
            }

            // clean input
            input_search.value = "";
            input_syno.checked = false;
        });
});
