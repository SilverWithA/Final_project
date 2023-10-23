import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../login/style/Login.css";
import { signInApi } from "../../api";

const Login = () => {
  const [userId, setUserId] = useState("");
  const [userPassword, setUserPassword] = useState("");
  const navigate = useNavigate();

  const SignInHandler = async (e) => {
    e.preventDefault();

    const data = {
      userId,
      userPassword,
    };

    if (userId.length === 0 || userPassword.length === 0) {
      alert("아이디와 비밀번호를 입력하세요");
      return;
    }

    const signInResponse = await signInApi(data);

    if (!signInResponse) {
      console.log(signInResponse);
      setUserId("");
      setUserPassword("");
      alert("로그인을 실패했습니다.");
      return;
    }
    if (!signInResponse.result) {
      console.log(signInResponse);
      setUserId("");
      setUserPassword("");
      alert(`${signInResponse.message}`);
      return;
    }
    console.log("로그인 성공");

    const { token, exprTime, user, widgetOne, widgetTwo } = signInResponse.data;
    const expires = new Date();
    expires.setMilliseconds(expires.getMilliseconds() + exprTime);

    // 위젯 1,2 의 true 값이 뭔지 찾는 부분
    const widgetOneTrue = Object.keys(widgetOne).find((key) => {
      return widgetOne[key] === true;
    });

    const widgetTwoTrue = Object.keys(widgetTwo).find((key) => {
      return widgetTwo[key] === true;
    });

    console.log(widgetOneTrue);
    console.log(widgetTwoTrue);
    sessionStorage.setItem("token", token, { expires });
    sessionStorage.setItem("user", user.userId);
    sessionStorage.setItem("widgetOneTrue", widgetOneTrue, { expires });
    sessionStorage.setItem("widgetTwoTrue", widgetTwoTrue, { expires });
    // setCookies("token", token, { expires });
    // setCookies("widgetOneTrue", widgetOneTrue, { expires });
    // setCookies("widgetTwoTrue", widgetTwoTrue);
    // setUser(user);

    navigate(`/`);
  };

  return (
    <div class="hihi">
      <form class="px-4 py-3">
        <div class="mb-3">
          <div
            style={{ fontFamily: "omyu_pretty, sans-serif", fontSize: "18px" }}
          >
            아이디
          </div>

          <input
            style={{ fontFamily: "omyu_pretty, sans-serif", fontSize: "18px" }}
            type="ID"
            class="form-control"
            id="exampleDropdownFormEmail1"
            placeholder="ID를 입력해주세요"
            onChange={(e) => setUserId(e.target.value)}
            value={userId}
          />
        </div>
        <div class="mb-3">
          <label for="exampleDropdownFormPassword1" class="form-label">
            <div
              style={{
                fontFamily: "omyu_pretty, sans-serif",
                fontSize: "18px",
              }}
            >
              비밀번호
            </div>
          </label>
          <input
            style={{ fontFamily: "omyu_pretty, sans-serif", fontSize: "18px" }}
            type="password"
            class="form-control"
            id="exampleDropdownFormPassword1"
            placeholder="비밀번호를 입력해주세요"
            onChange={(e) => setUserPassword(e.target.value)}
            value={userPassword}
          />
        </div>

        <div class="hihi">
          <button
            type="submit"
            class="btn btn-primary"
            style={{
              fontFamily: "omyu_pretty, sans-serif",
              fontSize: "18px",
              backgroundColor: "#970000",
              color: "white",
              border: 0,
            }}
            onClick={(e) => SignInHandler(e)}
          >
            로그인하기
          </button>
          <br></br>
          <div
            style={{ fontFamily: "omyu_pretty, sans-serif", fontSize: "20px" }}
          >
            홈페이지 이용이 처음이신가요?
          </div>
          <br></br>

          <Link to="/login/SignUp">
            <button
              type="submit"
              class="btn btn-primary"
              style={{ backgroundColor: "#970000",
              color: "white",
              border: 0 }}
            >
              <div
                style={{
                  fontFamily: "omyu_pretty, sans-serif",
                  fontSize: "18px",
                }}
              >
                지금 회원가입하기
              </div>
            </button>
          </Link>
        </div>
      </form>
    </div>
  );
};

export default Login;

// // 예제: fetch를 사용한 POST 요청
// fetch('/api/login', {
//   method: 'POST',
//   headers: {
//     'Content-Type': 'application/json',
//   },
//   body: JSON.stringify({ email: 'user@example.com', password: 'password' }),
// })
//   .then(response => response.json())
//   .then(data => {
//     // 서버 응답에 대한 처리
//   })
//   .catch(error => {
//     // 오류 처리
//   });
