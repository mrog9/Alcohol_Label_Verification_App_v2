// global variables

let currentController = null;
let pic_json = null;
// ------------------------------------------------------------

// in this method the image selected is processed so that the info
// is available for validation once form is submitted

async function get_pict_info(file) {

    let processed_data = null

    if (currentController) {
        currentController.abort();
    }
    currentController = new AbortController();

    const formData = new FormData();
    formData.append("file", file);

    await fetch("/preview_img", {
        method: "POST",
        body: formData,
        signal: currentController.signal
    })
    .then(response => response.json())
    .then(data => {
        
        pic_json = JSON.stringify(data);
    })
    .catch(err => {
        if (err.name === "AbortError") {
        console.log("Previous upload aborted");
        } else {
        console.error("Upload error:", err);
        }
    });

}

// -------------------------------------------------------------

// method sends the form data along with the processed image data to
// /validate route. validation info is returned

async function postData(){

    let validation_info = null;

    let form_info={

        brand : null,
        product : null,
        content : null,
        net: null

    };



    const b_tag = document.getElementById("brand");
    const p_tag = document.getElementById("product");
    const a_tag = document.getElementById("content");
    const n_tag = document.getElementById("net");

    form_info["brand"] = b_tag.value;
    form_info["product"] = p_tag.value;
    form_info["content"] = a_tag.value;
    form_info["net"] = n_tag.value;

    console.log(n_tag.value);

    const form_info_json = JSON.stringify(form_info);

    const all_info = {

        form : form_info_json,
        image: pic_json
    };

    await fetch("/validate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(all_info),
    })
    .then(response => response.json())
    .then(data=>{

        validation_info = data;

    })
    .catch(err => {
        if (err.name === "AbortError") {
        console.log("Previous upload aborted");
        } else {
        console.error("Upload error:", err);
        }
    });

    return validation_info;

}

// ------------------------------------------------------------

// in this method, i am displaying the validation comments on the html page

function display_validation_info(val_info){

    const missing_error = val_info['comment']['missing_headers'];
    const pic_err = val_info['comment']['comments_after_submit']

    console.log(val_info);

    let bt = document.getElementById('b')
    let pt = document.getElementById('p')
    let at = document.getElementById('a')
    let nt = document.getElementById('n')

    const bc = missing_error['brand']
    const pc = missing_error['product']
    const ac = missing_error['alcohol']
    const nc = missing_error['contents']

    if (bc || pc || ac || nc){

        if (bc){
            bt.hidden = false;
            bt.textContent = bc;

        }

        if (pc){
            pt.hidden = false;
            pt.textContent = pc;

        }

        if (ac){
            at.hidden = false;
            at.textContent = ac;

        }

        if (nc){
            nt.hidden = false;
            nt.textContent = nc;

        }


    }else if (pic_err){

        let e_tag = document.getElementById("failure");
        e_tag.hidden = false
        let h_tag = e_tag.getElementsByTagName('h1')[0];
        h_tag.textContent = pic_err;

        let i_tag = document.getElementById("preview_image");
        i_tag.src = "static/" + val_info['filepath'];

    }else{

        const wp = document.getElementById("whole_page")
        wp.style.display = "none"

        const st = document.getElementById("success")
        st.hidden = false

        const but = document.getElementById('reset')
        but.addEventListener('click',()=>{
            location.reload()
        })
        


    }

}

// ----------------------------------------------------------

// anytime a different file is selected this event is activated
// and new image is previewed and processed

const input = document.getElementById("fileInput");
  input.onchange = function(event) {


    let preview = document.getElementById("preview");
    preview.hidden = false;
    const preview_tag = document.getElementById("preview_image")
    preview_tag.src = URL.createObjectURL(event.target.files[0])

    get_pict_info(event.target.files[0]);

  };

//   ----------------------------------------------------------

// when a form is submitted this event is activated

const form = document.getElementById("form");
  form.onsubmit = function(event){

    event.preventDefault();

    document.getElementById('b').textContent = "";
    document.getElementById('p').textContent = "";
    document.getElementById('a').textContent = "";
    document.getElementById('n').textContent = "";

    if (pic_json){

        postData().then(val_info => display_validation_info(val_info));

    }else{

        const file_comm_tag = document.getElementById("form_upload_err");
        file_comm_tag.textContent = "Upload File and Complete the Form";

    }
  };