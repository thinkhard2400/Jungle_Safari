const headerArea = document.getElementById("header-area");

headerArea.innerHTML = `
    <div class="
        bg-black/50
        ">    

    <header class="
        h-[54px]
        px-[30px]

        flex
        items-center
        justify-between
    ">

        <div class="
            flex
            items-center
            gap-[12px]
        ">
            <img
                src="./images/account_circle.svg"
                class="
                    h-[35px]
                    w-[35px]
                ">

            <span class="
                text-[20px]
                leading-none
                font-light
            ">
            <span
                id="header-user-name"
                class="font-bold"
                ></span>님 안녕하세요!
            </span>
        </div>

        <button
            id="menu-button"
            class="ml-auto">
            <img
                src="./images/menu.svg"
                class="
                    h-[28px]
                    w-[28px]
                ">
        </button>
    </header>

    <div class="
        mx-[20px]
        h-[1px]
        bg-white/20
    "></div>
    <div
        id="drawer-overlay"
        class="
            hidden
            fixed
            inset-0

            bg-black/60
        "
    ></div>
    <div
        id="drawer"
        class="
            hidden
            fixed
            top-0
            right-0
            bottom-0

            w-[75%]

            bg-[#111111]
            text-white
        ">

        <div class="
            pt-[100px]
            px-[36px]

            flex
            flex-col
            items-center
        ">

            <div class="
                flex
                items-center
                gap-[12px]
            ">
                <img
                    src="./images/account_circle.svg"
                    class="
                        h-[35px]
                        w-[35px]
                    ">
                 <span
                    id="drawer-user-name"
                    class="
                        text-[20px]
                        font-bold
                    "
                ></span>
            </div>
            <div class="
                mt-[70px]

                flex
                flex-col
                items-center
                gap-[42px]
            ">
                <button 
                    onclick="location.href='./mypage.html'"
                    class="
                        text-[20px]
                        font-bold
                        text-white
                    ">
                        기록 확인하기
                </button>
                <button 
                    onclick="location.href='./index.html'"
                    class="
                    text-[20px]
                    font-bold
                    text-white
                ">
                    로그아웃
                </button>
            </div>
        </div>
    </div>
`;


const menuButton = document.getElementById("menu-button");
const drawer = document.getElementById("drawer");
const drawerOverlay = document.getElementById("drawer-overlay");

storeReady.then(() => {
    document.getElementById("header-user-name").textContent =
        user.name;

    document.getElementById("drawer-user-name").textContent =
        `${user.name}님`;
});

menuButton.addEventListener("click", () => {
    drawer.classList.remove("hidden");
    drawerOverlay.classList.remove("hidden");
});


drawerOverlay.addEventListener("click", () => {
    drawer.classList.add("hidden");
    drawerOverlay.classList.add("hidden");
});