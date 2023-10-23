import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../login/style/SignUp.css";
import { signUpApi } from "../../api";

const SignUp = () => {
  const [userId, setUserId] = useState("");
  const [userPassword, setUserPassword] = useState("");
  const [userPasswordCheck, setUserPasswordCheck] = useState("");
  const navigate = useNavigate();

  const SignUpHandler = async (e) => {
    e.preventDefault();

    if (userId.length === 0 || userPassword.length === 0) {
      alert("이메일과 비밀번호를 입력하세요");
      return;
    }

    const data = {
      userId,
      userPassword,
      userPasswordCheck,
    };

    const signUpResponse = await signUpApi(data);

    if (!signUpResponse) {
      console.log(signUpResponse);
      setUserId("");
      setUserPassword("");
      setUserPasswordCheck("");
      alert("회원가입 실패");
      return;
    }
    if (!signUpResponse.result) {
      console.log(signUpResponse);
      alert(signUpResponse.message);
      setUserId("");
      setUserPassword("");
      setUserPasswordCheck("");
      return;
    }
    alert("회원가입 성공");
    console.log(signUpResponse);
    navigate(`/login/Login`);
  };
  return (
    <div className="gdgd">
      <form class="px-4 py-3">
        <div class="mb-3">
          <div
            style={{ fontFamily: "omyu_pretty, sans-serif", fontSize: "20px" }}
          >
            아이디
          </div>

          <input
            type="ID"
            class="form-control"
            id="exampleDropdownFormEmail1"
            onChange={(e) => setUserId(e.target.value)}
            value={userId}
          />
        </div>
        <div class="mb-3">
          <label for="exampleDropdownFormPassword1" class="form-label">
            <div
              style={{
                fontFamily: "omyu_pretty, sans-serif",
                fontSize: "20px",
              }}
            >
              비밀번호
            </div>
          </label>
          <input
            type="password"
            class="form-control"
            id="exampleDropdownFormPassword1"
            onChange={(e) => setUserPassword(e.target.value)}
            value={userPassword}
          />
        </div>
        <div class="mb-3">
          <label for="exampleDropdownFormPassword2" class="form-label">
            <div
              style={{
                fontFamily: "omyu_pretty, sans-serif",
                fontSize: "20px",
              }}
            >
              비밀번호 확인
            </div>
          </label>
          <input
            type="password"
            class="form-control"
            id="exampleDropdownFormPassword2"
            onChange={(e) => setUserPasswordCheck(e.target.value)}
            value={userPasswordCheck}
          />
        </div>
        

        <button
          type="submit"
          class="btn btn-primary"
          style={{
            backgroundColor: "#970000",
            color: "white",
            border: 0,
            fontFamily: "omyu_pretty, sans-serif",
            fontSize: "18px",
            marginLeft:"33%"
          }}
          onClick={(e) => SignUpHandler(e)}
        >
          <div
            style={{
              fontFamily: "omyu_pretty, sans-serif",
              fontSize: "18px",
              
            }}
          >
            회원가입
          </div>
        </button>
      </form>
    </div>
  );
};

export default SignUp;
