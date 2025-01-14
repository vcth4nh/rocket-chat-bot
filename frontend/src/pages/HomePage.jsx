import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  TextField,
  Button,
  Grid,
  Paper,
  IconButton,
  Switch,
  FormControlLabel,
} from "@mui/material";

import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import {
  getPoliciesByType,
  createPolicy,
  updatePolicy,
  deletePolicy,
} from "../services/policyService";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const HomePage = () => {
  const [blacklist, setBlacklist] = useState([]);
  const [regexList, setRegexList] = useState([]);
  const [newWords, setNewWords] = useState("");
  const [newRegex, setNewRegex] = useState("");
  const [editingRegex, setEditingRegex] = useState(null);
  const [editingBlacklist, setEditingBlacklist] = useState(null);
  const [detectSecrets, setDetectSecrets] = useState(false);
  const [wordLimit, setWordLimit] = useState(0);

  useEffect(() => {
    handleLoadBlacklist();
    handleLoadRegexList();
    handleLoadDetectSecrets();
    handleLoadWordLimit();
  }, []);

  const handleLoadBlacklist = async () => {
    try {
      const data = await getPoliciesByType("blacklist");
      const items = Array.isArray(data)
        ? data.map((item) => ({
            id: item._id,
            value: item.value,
            type: item.type,
            createdAt: item.created_at,
            updatedAt: item.updated_at,
          }))
        : [];
      setBlacklist(items);
    } catch (err) {
      console.error("Failed to load blacklist:", err);
    }
  };

  const handleLoadRegexList = async () => {
    try {
      const data = await getPoliciesByType("regex");
      const items = Array.isArray(data)
        ? data.map((item) => ({
            id: item._id,
            value: item.value,
            type: item.type,
            createdAt: item.created_at,
            updatedAt: item.updated_at,
          }))
        : [];
      setRegexList(items);
    } catch (err) {
      console.error("Failed to load regex:", err);
    }
  };

  const handleLoadDetectSecrets = async () => {
    try {
      const data = await getPoliciesByType("detect_secrets");
      const item = data[0].value;
      setDetectSecrets(item);
    } catch (err) {
      console.error("Failed to load detect secrets:", err);
    }
  };

  const handleLoadWordLimit = async () => {
    try {
      const data = await getPoliciesByType("length_limit");
      const item = data[0].value;
      setWordLimit(item);
    } catch (err) {
      console.error("Failed to load word limit:", err);
    }
  };

  const handleBlacklistChange = async () => {
    const words = newWords
      .split("\n")
      .map((word) => word.trim())
      .filter((word) => word);

    try {
      await Promise.all(
        words.map((word) => createPolicy({ type: "blacklist", value: word }))
      );
      handleLoadBlacklist();
      setNewWords("");
      toast.success("Lưu từ blacklist thành công!");
    } catch (error) {
      console.error("Error while updating blacklist:", error.message || error);
      toast.error("Lỗi khi lưu từ blacklist!");
    }
  };

  const handleRegexChange = async () => {
    const regexLines = newRegex
      .split("\n")
      .map((regex) => regex.trim())
      .filter(Boolean);

    try {
      await Promise.all(
        regexLines.map((regex) => createPolicy({ type: "regex", value: regex }))
      );
      handleLoadRegexList();
      setNewRegex("");
      toast.success("Lưu regex blacklist thành công!");
    } catch (error) {
      console.error("Error while updating regex:", error.message || error);
      toast.error("Lỗi khi lưu regex blacklist!");
    }
  };

  const handleEditRegex = (index) => {
    const regexToEdit = regexList[index - 1];
    setEditingRegex({ index, value: regexToEdit.value, id: regexToEdit.id });
  };

  const handleEditBlacklist = (index) => {
    const blacklistToEdit = blacklist[index - 1];
    setEditingBlacklist({
      index,
      value: blacklistToEdit.value,
      id: blacklistToEdit.id,
    });
  };

  const handleSaveEditRegex = async () => {
    if (editingRegex) {
      try {
        await updatePolicy(editingRegex.id, {
          type: "regex",
          value: editingRegex.value,
        });
        toast.success("Lưu regex blacklist thành công!");
      } catch (error) {
        console.error("Error while updating regex:", error.message || error);
        toast.error("Lỗi khi lưu regex blacklist!");
      }
      handleLoadRegexList();
      setEditingRegex(null);
    }
  };

  const handleSaveEditBlacklist = async () => {
    if (editingBlacklist) {
      try {
        await updatePolicy(editingBlacklist.id, {
          value: editingBlacklist.value,
          type: "blacklist",
        });
        toast.success("Lưu từ blacklist thành công!");
      } catch (error) {
        console.error("Error while updating regex:", error.message || error);
        toast.error("Lỗi khi lưu từ blacklist!");
      }
      handleLoadBlacklist();
      setEditingBlacklist(null);
    }
  };

  const handleSaveToggleAndLimit = async () => {
    try {
      await createPolicy({
        type: "detect_secrets",
        value: Boolean(detectSecrets),
      });
      await createPolicy({
        type: "length_limit",
        value: parseInt(wordLimit, 10),
      });
      toast.success("Lưu cấu hình chung thành công!");
    } catch (error) {
      console.error(
        "Error while updating detect secrets:",
        error.message || error
      );
      toast.error("Lỗi khi lưu cấu hình chung!");
    }
  };

  const handleDeleteBlacklist = async (id) => {
    try {
      await deletePolicy(id);
      handleLoadBlacklist();
    } catch (error) {
      console.error("Error while deleting blacklist:", error.message || error);
    }
  };

  const handleDeleteRegex = async (id) => {
    try {
      await deletePolicy(id);
      handleLoadRegexList();
    } catch (error) {
      console.error("Error while deleting regex:", error.message || error);
    }
  };

  const blacklistColumns = [
    { field: "index", headerName: "STT", width: 100 },
    { field: "value", headerName: "Từ blacklist", flex: 1 },
    {
      field: "actions",
      headerName: "Hành động",
      width: 150,
      renderCell: (params) => (
        <Box>
          <IconButton
            color="primary"
            onClick={() => handleEditBlacklist(params.row.index)}
          >
            <EditIcon />
          </IconButton>
          <IconButton
            color="error"
            onClick={() => handleDeleteBlacklist(params.row.id)}
          >
            <DeleteIcon />
          </IconButton>
        </Box>
      ),
    },
  ];

  const blacklistRows = blacklist.map((item, index) => ({
    id: item.id,
    index: index + 1,
    value: item.value,
    type: item.type,
    createdAt: item.createdAt,
    updatedAt: item.updatedAt,
  }));

  const regexColumns = [
    { field: "index", headerName: "STT", width: 100 },
    { field: "value", headerName: "Regex Pattern", flex: 1 },
    {
      field: "actions",
      headerName: "Hành động",
      width: 150,
      renderCell: (params) => (
        <Box>
          <IconButton
            color="primary"
            onClick={() => handleEditRegex(params.row.index)}
          >
            <EditIcon />
          </IconButton>
          <IconButton
            color="error"
            onClick={() => handleDeleteRegex(params.row.id)}
          >
            <DeleteIcon />
          </IconButton>
        </Box>
      ),
    },
  ];

  const regexRows = regexList.map((regex, index) => ({
    id: regex.id,
    index: index + 1,
    value: regex.value,
    type: regex.type,
    createdAt: regex.createdAt,
    updatedAt: regex.updatedAt,
  }));

  return (
    <Box
      sx={{
        p: 4,
        maxWidth: "1200px",
        margin: "0 auto",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        gap: 4,
      }}
    >
      <ToastContainer position="top-right" autoClose={3000} />
      <Typography variant="h4" color="primary" gutterBottom>
        Cấu hình Policy ChatGPT
      </Typography>

      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Cấu hình chung
        </Typography>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={6}>
            <FormControlLabel
              control={
                <Switch
                  checked={detectSecrets}
                  onChange={(e) => setDetectSecrets(e.target.checked)}
                />
              }
              label="Phát hiện Secrets"
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              fullWidth
              variant="outlined"
              label="Giới hạn từ ngữ"
              type="number"
              value={wordLimit}
              onChange={(e) => setWordLimit(e.target.value)}
            />
          </Grid>
        </Grid>
        <Box sx={{ mt: 2 }}>
          <Button
            variant="contained"
            color="secondary"
            onClick={handleSaveToggleAndLimit}
          >
            Lưu cấu hình
          </Button>
        </Box>
      </Paper>

      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Cấu hình từ blacklist
        </Typography>
        {editingBlacklist && (
          <Box sx={{ mb: 2 }}>
            <TextField
              fullWidth
              variant="outlined"
              value={editingBlacklist.value}
              onChange={(e) =>
                setEditingBlacklist({
                  ...editingBlacklist,
                  value: e.target.value,
                })
              }
              placeholder="Thay đổi từ blacklist"
              sx={{ mb: 1 }}
            />
            <Button
              variant="contained"
              color="secondary"
              onClick={handleSaveEditBlacklist}
            >
              Lưu thay đổi
            </Button>
          </Box>
        )}
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={6}>
            <TextField
              fullWidth
              variant="outlined"
              value={newWords}
              onChange={(e) => setNewWords(e.target.value)}
              placeholder="Nhập từ blacklist (mỗi từ trên một dòng)"
              multiline
              rows={2}
              sx={{ mb: 2 }}
            />
            <Button
              variant="contained"
              color="secondary"
              onClick={handleBlacklistChange}
            >
              Lưu thay đổi
            </Button>
          </Grid>
          <Grid item xs={6}>
            <Box sx={{ height: 400, mt: 2 }}>
              <DataGrid
                rows={blacklistRows}
                columns={blacklistColumns}
                pageSize={5}
                rowsPerPageOptions={[5]}
                disableSelectionOnClick
                components={{ Toolbar: GridToolbar }}
                disableColumnFilter
                disableColumnSelector
                disableDensitySelector
                slots={{ toolbar: GridToolbar }}
                slotProps={{
                  toolbar: {
                    showQuickFilter: true,
                  },
                }}
              />
            </Box>
          </Grid>
        </Grid>
      </Paper>

      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Cấu hình regex blacklist
        </Typography>
        {editingRegex && (
          <Box sx={{ mb: 2 }}>
            <TextField
              fullWidth
              variant="outlined"
              value={editingRegex.value}
              onChange={(e) =>
                setEditingRegex({ ...editingRegex, value: e.target.value })
              }
              placeholder="Nhập regex pattern"
              sx={{ mb: 1 }}
            />
            <Button
              variant="contained"
              color="secondary"
              onClick={handleSaveEditRegex}
            >
              Lưu thay đổi
            </Button>
          </Box>
        )}
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={6}>
            <TextField
              fullWidth
              variant="outlined"
              value={newRegex}
              onChange={(e) => setNewRegex(e.target.value)}
              placeholder="Nhập regex pattern (mỗi pattern trên một dòng)"
              multiline
              rows={4}
              sx={{ mb: 2 }}
            />
            <Button
              variant="contained"
              color="secondary"
              onClick={handleRegexChange}
            >
              Lưu thay đổi
            </Button>
          </Grid>
          <Grid item xs={6}>
            <Box sx={{ height: 400, mt: 2 }}>
              <DataGrid
                rows={regexRows}
                columns={regexColumns}
                pageSize={5}
                rowsPerPageOptions={[5]}
                disableSelectionOnClick
                disableColumnFilter
                disableColumnSelector
                disableDensitySelector
                slots={{ toolbar: GridToolbar }}
                slotProps={{
                  toolbar: {
                    showQuickFilter: true,
                  },
                }}
              />
            </Box>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default HomePage;
